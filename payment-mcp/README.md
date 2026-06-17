# Payment MCP learning sample

This project shows the basic flow:

```text
User
  -> CLI Chatbot
  -> MCP Client, discovers tools
  -> MCP Server, exposes tools
  -> Dummy Bank Service
```

The sample use case is a user making a payment from account `101` to receiver `999`.
The dummy bank has enough balance in `101`, so the payment succeeds.

## Run

```powershell
.\.venv\Scripts\python chatbot\ai_chat.py
```

Then type:

```text
sample
```

Or call individual commands:

```text
tools
balance 101
pay 101 999 1000
status PAY-0001
```

## Where the pieces live

- `chatbot/ai_chat.py`: CLI chatbot. For learning, it routes commands without an LLM key.
- `chatbot/mcp_client.py`: starts the MCP server over stdio, discovers tools, and calls tools.
- `mcp-server/server.py`: exposes MCP tools.
- `mcp-server/tools/*.py`: thin MCP tool functions.
- `bank-service/payment_engine.py`: dummy bank infrastructure with success and failed payment paths.

## Groq or Claude?

For a real natural-language chatbot, this sample uses GroqCloud's
OpenAI-compatible chat completions API with `llama-3.3-70b-versatile`.
It fits this Python sample well:
the MCP client first asks the MCP server for available tools, converts those discovered
MCP tool schemas into chat function definitions, and asks the model which discovered
tool to call.

When you add a real AI chatbot:

Set your key:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

Run:

```powershell
.\.venv\Scripts\python chatbot\ai_chat.py
```

Try:

```text
transfer 1000 from account 101 to receiver 999
```

Claude would also work, but you would write a different `llm_router.py` for Anthropic's SDK.
The MCP server, MCP client, and bank service would stay the same.

## Runtime sequence

```text
User -> AI chatbot: transfer 1000 from account 101 to receiver 999
MCP client -> MCP server: ListToolsRequest
MCP server -> MCP client: create_payment, get_balance, payment_status schemas
AI -> MCP client: choose create_payment with from_account=101, receiver_account=999, amount=1000
MCP client -> MCP server: CallToolRequest create_payment
MCP server -> Dummy bank: process payment
Dummy bank -> MCP server: success
MCP server -> MCP client: CallToolResult
AI chatbot -> User: payment successful
```
