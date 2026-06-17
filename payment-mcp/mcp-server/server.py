from mcp.server.fastmcp import FastMCP

from tools.account_balance import get_balance
from tools.create_payment import create_payment
from tools.payment_status import payment_status


mcp = FastMCP("payment-mcp")


mcp.tool()(create_payment)
mcp.tool()(get_balance)
mcp.tool()(payment_status)


if __name__ == "__main__":
    mcp.run()
