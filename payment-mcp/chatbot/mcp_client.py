import json
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).resolve().parents[1] / "mcp-server" / "server.py"


class PaymentMcpClient:
    def __init__(self) -> None:
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None

    async def __aenter__(self) -> "PaymentMcpClient":
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_PATH)],
        )
        read, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.exit_stack.aclose()

    async def list_tools(self) -> list[str]:
        if self.session is None:
            raise RuntimeError("MCP client is not connected")
        result = await self.session.list_tools()
        return [tool.name for tool in result.tools]

    async def list_tool_specs(self) -> list[dict]:
        if self.session is None:
            raise RuntimeError("MCP client is not connected")
        result = await self.session.list_tools()
        return [tool.model_dump() for tool in result.tools]

    async def call_tool(self, name: str, arguments: dict) -> dict:
        if self.session is None:
            raise RuntimeError("MCP client is not connected")
        result = await self.session.call_tool(name, arguments)
        if not result.content:
            return {}

        text = getattr(result.content[0], "text", "{}")
        return json.loads(text)


def pretty(data: dict | list) -> str:
    return json.dumps(data, indent=2)
