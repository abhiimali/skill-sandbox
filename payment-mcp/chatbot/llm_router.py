import json
import os
import re

from openai import OpenAI


MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

SYSTEM_PROMPT = """
You are a payment assistant connected to MCP tools.
Use the discovered MCP tools when the user asks about payments, balances, or payment status.

Important payment rules:
- If the user says "my account" and does not give a sender account, use account 101.
- If the user asks to pay receiver 999, use receiver_account 999.
- Never invent an amount. Ask the user for the amount if it is missing.
- For this learning demo, a payment from account 101 to receiver 999 should use the discovered payment tool.
"""


def mcp_tools_to_chat_tools(mcp_tools: list[dict]) -> list[dict]:
    chat_tools = []
    for tool in mcp_tools:
        input_schema = tool.get("inputSchema") or {"type": "object", "properties": {}}
        input_schema.setdefault("type", "object")
        input_schema.setdefault("properties", {})

        chat_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description") or f"Call MCP tool {tool['name']}.",
                "parameters": input_schema,
            },
        })
    return chat_tools


def route_failed_tool_generation(error: Exception, mcp_tools: list[dict]) -> dict | None:
    error_text = str(error)
    match = re.search(r"<function=([a-zA-Z_][\w]*)\((.*?)\)</function>", error_text)
    if match is None:
        return None

    tool_names = {tool["name"] for tool in mcp_tools}
    tool_name = match.group(1)
    if tool_name not in tool_names:
        return None

    try:
        arguments = json.loads(match.group(2))
    except json.JSONDecodeError:
        return None

    return {
        "tool_name": tool_name,
        "arguments": arguments,
        "message": None,
    }


class LlmRouter:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url=GROQ_BASE_URL,
        )

    def choose_tool(self, user_message: str, mcp_tools: list[dict]) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                tools=mcp_tools_to_chat_tools(mcp_tools),
            )
        except Exception as exc:
            routed = route_failed_tool_generation(exc, mcp_tools)
            if routed is not None:
                return routed
            raise

        message = response.choices[0].message
        tool_calls = message.tool_calls or []

        if not tool_calls:
            return {
                "tool_name": None,
                "arguments": {},
                "message": message.content or "Please ask me to make a payment, check balance, or check status.",
            }

        tool_call = tool_calls[0]
        return {
            "tool_name": tool_call.function.name,
            "arguments": json.loads(tool_call.function.arguments),
            "message": None,
        }

    def summarize_tool_result(self, user_message: str, tool_name: str, result: dict) -> str:
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Explain MCP tool results to the user in one short sentence."},
                {"role": "user", "content": user_message},
                {
                    "role": "assistant",
                    "content": (
                        f"MCP tool called: {tool_name}\n"
                        f"MCP tool result: {json.dumps(result)}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content or json.dumps(result)


def llm_is_configured() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))
