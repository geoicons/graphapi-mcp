"""Load Graph API RequestRocket proxy credentials from env files or the process environment."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_PACKAGE_DIR = Path(__file__).resolve().parent


def _resolve_dotenv_path() -> Path | None:
    override = os.environ.get("DOTENV_PATH")
    if override:
        return Path(override).expanduser()
    config_env = _PACKAGE_DIR / "config.env"
    if config_env.is_file():
        return config_env
    dot_env = _PACKAGE_DIR / ".env"
    if dot_env.is_file():
        return dot_env
    return None


_env_file = _resolve_dotenv_path()
if _env_file is not None:
    load_dotenv(_env_file)

_raw_url = os.environ.get("GRAPH_API_REQUESTROCKET_URL", "").strip()
_raw_key = os.environ.get("GRAPH_API_REQUESTROCKET_KEY", "").strip()

if not _raw_url or not _raw_key:
    missing = []
    if not _raw_url:
        missing.append("GRAPH_API_REQUESTROCKET_URL")
    if not _raw_key:
        missing.append("GRAPH_API_REQUESTROCKET_KEY")
    hint = (
        f"Set {', '.join(missing)} in the environment or in "
        f"`config.env` / `.env` next to server.py "
        f"(or set DOTENV_PATH to your credentials file)."
    )
    raise RuntimeError(
        "Missing Graph API RequestRocket configuration: "
        + ", ".join(missing)
        + ". "
        + hint
    )

BASE_URL = _raw_url.rstrip("/")
AUTH_KEY = _raw_key
