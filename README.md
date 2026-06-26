# Payment MCP Chatbot

A small learning project that connects a natural-language payment chatbot to backend tools using MCP. The chatbot uses GroqCloud (`llama-3.3-70b-versatile`) to understand user intent, route requests to MCP tools, and return friendly responses.

## What It Does

- Creates dummy payments between accounts.
- Checks account balances.
- Looks up payment status.
- Uses MCP client/server flow to expose backend actions as tools.

## Architecture

```text
User
  -> CLI Chatbot
  -> LLM Router using GroqCloud
  -> MCP Client
  -> MCP Server
  -> Payment Tools
  -> Dummy Bank Service
```

## Project Structure

```text
chatbot/
  ai_chat.py       # CLI chatbot
  llm_router.py    # Groq LLM routing and summaries
  mcp_client.py    # MCP client over stdio

mcp-server/
  server.py        # MCP tool server
  tools/           # create_payment, get_balance, payment_status

bank-service/
  payment_engine.py # In-memory dummy bank
```

## Setup

Set your Groq API key:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

Install dependencies if needed:

```powershell
.\.venv\Scripts\pip install -r chatbot\requirements.txt
.\.venv\Scripts\pip install -r mcp-server\requirements.txt
```

## Run

From the `payment-mcp` folder:

```powershell
.\.venv\Scripts\python chatbot\ai_chat.py
```

Try prompts like:

```text
transfer 870 from my account to receiver 999
what is the balance of account 101?
check status PAY-0001
```

## Example Response

```text
Done. Your payment of INR 870.0 from account 101 to account 999 was successful. Payment ID: PAY-0001.
```

## Sample Output 

<img width="921" height="391" alt="image" src="https://github.com/user-attachments/assets/42df92e2-1263-48da-a82b-7022fbd4c4fa" />

