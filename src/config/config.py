# GROUP: config
# DESCRIPTION: Core config for Shadow AI system (Telegram + Webhook + Google infra)

import json
import os
from dataclasses import dataclass
from typing import Any, List

from src.config.base import get_env


# =========================
# TELEGRAM
# =========================

@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str
    webhook_url: str
    bot_username: str
    admin_ids: List[int]
    mods_ids: List[int]
    chat_ids: List[str]


# =========================
# AI / LLM PROVIDERS
# =========================

@dataclass
class AIConfig:
    gemini_api_key: str | None


# =========================
# GOOGLE
# =========================

@dataclass
class GoogleSearchConfig:
    api_key: str | None
    cx: str | None


@dataclass
class GoogleConfig:
    service_account: dict[str, Any] | None
    search: GoogleSearchConfig
    docs_id: str | None
    drive_root_folder: str | None
    sheet_id: str | None


# =========================
# SEARCH / TOOLS
# =========================

@dataclass
class ToolsConfig:
    searx_url: str | None
    tavily_api_key: str | None


# =========================
# ROOT
# =========================

@dataclass
class Config:
    telegram: TelegramConfig
    google: GoogleConfig
    ai: AIConfig
    tools: ToolsConfig
    demo_mode: bool


# =========================
# HELPERS
# =========================

def _parse_json(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None

    data = json.loads(value)

    if not isinstance(data, dict):
        raise ValueError("Invalid JSON object")

    if "private_key" in data:
        data["private_key"] = data["private_key"].replace("\\n", "\n")

    return data


def _parse_list(value: str | None) -> List[str]:
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def _parse_int_list(value: str | None) -> List[int]:
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def _parse_bool(value: str | None) -> bool:
    return str(value).lower() in ("1", "true", "yes", "y", "on")


# =========================
# LOAD CONFIG
# =========================

def load_config() -> Config:
    return Config(
        telegram=TelegramConfig(
            token=get_env("TELEGRAM_TOKEN"),
            webhook_secret=get_env("WEBHOOK_SECRET"),
            webhook_url=get_env("WEBHOOK_URL"),
            bot_username=get_env("BOT_USERNAME"),
            admin_ids=_parse_int_list(get_env("ADMIN_IDS", required=False)),
            mods_ids=_parse_int_list(get_env("MODS_IDS", required=False)),
            chat_ids=_parse_list(get_env("CHAT_IDS", required=False)),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                get_env("GOOGLE_SERVICE_ACCOUNT", required=False)
            ),
            search=GoogleSearchConfig(
                api_key=get_env("GOOGLE_SEARCH_API", required=False),
                cx=get_env("GOOGLE_SEARCH_CX", required=False),
            ),
            docs_id=get_env("GOOGLE_DOCS_ID", required=False),
            drive_root_folder=get_env("GOOGLE_DRIVE_ROOT_FOLDER", required=False),
            sheet_id=get_env("GOOGLE_SHEET_ID", required=False),
        ),
        ai=AIConfig(
            gemini_api_key=get_env("GEMINI_API_KEY", required=False),
        ),
        tools=ToolsConfig(
            searx_url=get_env("SEARX_URL", required=False),
            tavily_api_key=get_env("TAVILY_API_KEY", required=False),
        ),
        demo_mode=_parse_bool(get_env("DEMO_MODE", required=False)),
    )