import asyncio
import json

from llm_router import LlmRouter, llm_is_configured
from mcp_client import PaymentMcpClient


HELP = """Try:
  transfer 1000 from account 101 to receiver 999
  send 750 from my account to account 999
  what is the balance of account 101?
  check status PAY-0001
  show available tools
  exit
"""


def friendly_tool_result(tool_name: str, result: dict) -> str:
    if tool_name == "create_payment":
        payment_id = result.get("payment_id", "unknown")
        amount = result.get("amount")
        currency = result.get("currency", "")
        from_account = result.get("from_account", "the sender")
        receiver_account = result.get("receiver_account", "the receiver")

        if result.get("ok"):
            return (
                f"Done. Your payment of {currency} {amount} from account "
                f"{from_account} to account {receiver_account} was successful. "
                f"Payment ID: {payment_id}."
            )
        return (
            f"I could not complete the payment. {result.get('message', 'Please try again.')}"
        )

    if tool_name == "get_balance":
        if result.get("ok"):
            return (
                f"Account {result.get('account_id')} has a balance of "
                f"{result.get('currency', '')} {result.get('balance')}."
            )
        return result.get("message", "I could not fetch that balance.")

    if tool_name == "payment_status":
        if result.get("ok"):
            return (
                f"Payment {result.get('payment_id')} is {result.get('status')}. "
                f"Amount: {result.get('currency', '')} {result.get('amount')}."
            )
        return result.get("message", "I could not find that payment.")

    return result.get("message") or json.dumps(result)


async def execute_action(
    client: PaymentMcpClient,
    router: LlmRouter,
    user_message: str,
    routed: dict,
) -> None:
    tool_name = routed.get("tool_name")
    arguments = routed.get("arguments", {})

    if tool_name is None:
        print(routed["message"])
        return

    result = await client.call_tool(tool_name, arguments)
    try:
        print(router.summarize_tool_result(user_message, tool_name, result))
    except Exception:
        print(friendly_tool_result(tool_name, result))


async def main() -> None:
    if not llm_is_configured():
        print("GROQ_API_KEY is not set.")
        print("Set it first, then run this chatbot again:")
        print("$env:GROQ_API_KEY='your_api_key_here'")
        return

    router = LlmRouter()
    print("Payment MCP chatbot with Groq natural-language routing")
    print(HELP)

    async with PaymentMcpClient() as client:
        mcp_tools = await client.list_tool_specs()
        tool_names = [tool["name"] for tool in mcp_tools]
        print("MCP tools discovered:", ", ".join(tool_names))

        while True:
            try:
                user_message = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not user_message:
                continue
            if user_message.lower() in {"exit", "quit"}:
                break

            try:
                routed = router.choose_tool(user_message, mcp_tools)
                await execute_action(client, router, user_message, routed)
            except Exception as exc:
                print(f"Sorry, I could not process that request: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
