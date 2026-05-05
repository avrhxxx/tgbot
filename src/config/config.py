# src/config/config.py
# GROUP: config
# DESCRIPTION: Core config for Shadow AI system (Telegram + Webhook + Google infra)

import json
from dataclasses import dataclass
from typing import Any

from src.config.base import get_env


# =========================
# TELEGRAM
# =========================

@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str
    webhook_url: str


# =========================
# GOOGLE (FUTURE AI + INGESTION)
# =========================

@dataclass
class GoogleSearchConfig:
    api_key: str | None
    cx: str | None


@dataclass
class GoogleConfig:
    service_account: dict[str, Any] | None
    search: GoogleSearchConfig


# =========================
# ROOT
# =========================

@dataclass
class Config:
    telegram: TelegramConfig
    google: GoogleConfig


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


# =========================
# LOAD CONFIG
# =========================

def load_config() -> Config:
    return Config(
        telegram=TelegramConfig(
            token=get_env("TELEGRAM_TOKEN"),
            webhook_secret=get_env("WEBHOOK_SECRET"),
            webhook_url=get_env("WEBHOOK_URL"),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                get_env("GOOGLE_SERVICE_ACCOUNT", required=False)
            ),
            search=GoogleSearchConfig(
                api_key=get_env("GOOGLE_SEARCH_API_KEY", required=False),
                cx=get_env("GOOGLE_SEARCH_CX", required=False),
            ),
        ),
    )