"""MCP server exposing a single tool to call Microsoft Graph via a RequestRocket proxy."""

from __future__ import annotations

import httpx
from mcp.server.fastmcp import FastMCP

import config

mcp = FastMCP("graph-mcp")

_SUPPORTED_METHODS = frozenset({"GET", "POST", "PATCH", "PUT", "DELETE"})
_GRAPH_PREFIX = "https://graph.microsoft.com/v1.0"


def _normalize_graph_path(path: str) -> str:
    p = path.strip()
    plen = len(_GRAPH_PREFIX)
    if p.casefold().startswith(_GRAPH_PREFIX.casefold()):
        p = p[plen:].lstrip() or "/"
    if not p.startswith("/"):
        p = "/" + p
    return p


@mcp.tool()
async def graphapi(
    method: str,
    path: str,
    params: dict | None = None,
    body: dict | None = None,
) -> dict:
    """Call Microsoft Graph through the configured RequestRocket proxy."""
    verb = method.strip().upper()
    if verb not in _SUPPORTED_METHODS:
        return {
            "error": (
                f"Unsupported HTTP method {method!r}. "
                f"Use one of: {', '.join(sorted(_SUPPORTED_METHODS))}."
            )
        }

    norm_path = _normalize_graph_path(path)
    url = f"{config.BASE_URL}{norm_path}"
    headers = {
        "Authorization": config.AUTH_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if verb in ("GET", "DELETE"):
                response = await client.request(
                    verb, url, headers=headers, params=params
                )
            else:
                request_kwargs: dict = {"headers": headers}
                if params is not None:
                    request_kwargs["params"] = params
                if body is not None:
                    request_kwargs["json"] = body
                response = await client.request(verb, url, **request_kwargs)
    except httpx.RequestError as exc:
        return {"error": str(exc)}

    if 200 <= response.status_code < 300:
        try:
            data = response.json()
        except Exception:
            data = response.text
        return {"status": response.status_code, "data": data}

    return {"status": response.status_code, "error": response.text}


if __name__ == "__main__":
    print("Graph API MCP server started")
    print(f"Proxy: {config.BASE_URL}")
    print("Tool: graphapi(method, path, params?, body?)")
    mcp.run()
