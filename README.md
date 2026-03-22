# graph-mcp

Minimal Python MCP server that exposes one tool, `graphapi`, for authenticated Microsoft Graph API calls through a [RequestRocket](https://requestrocket.com) proxy.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `config.env` or `.env` in this directory (same folder as `server.py`) and set:

- `GRAPH_API_REQUESTROCKET_URL` — proxy base URL (no trailing slash required; it is stripped)
- `GRAPH_API_REQUESTROCKET_KEY` — authorization value sent as the `Authorization` header

Alternatively, set those variables in your environment. To load credentials from another file (for example Cowork’s `config.env`), set:

```bash
export DOTENV_PATH=/path/to/config.env
```

## Run

```bash
python server.py
```

The server uses stdio transport (FastMCP default). On startup it logs the proxy URL and tool signature to stdout.

## Tool: `graphapi`

| Argument | Description |
|----------|-------------|
| `method` | `GET`, `POST`, `PATCH`, `PUT`, or `DELETE` |
| `path` | Graph path such as `/me/messages`. A leading `https://graph.microsoft.com/v1.0` prefix is stripped. |
| `params` | Optional query parameters (e.g. `{"$top": 10}`) |
| `body` | Optional JSON body for `POST` / `PATCH` / `PUT` |

Successful responses return `{"status": <code>, "data": ...}` where `data` is parsed JSON or plain text if the body is not JSON. HTTP errors return `{"status": <code>, "error": "<body>"}`. Connection failures return `{"error": "<message>"}`.

## Cowork (local MCP)

Add a local MCP connector:

```text
python /path/to/graph-mcp/server.py
```

If credentials live elsewhere, set `DOTENV_PATH` to that file, for example:

```text
DOTENV_PATH=/Users/you/project/config.env
```

## Requirements

See `requirements.txt`: `mcp[cli]`, `httpx`, `python-dotenv`, `pydantic`.
