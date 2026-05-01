# src/config/config.py
# GROUP: config
# DESCRIPTION: MVP config for AI Wiki Bot (Telegram + Vertex AI + Firestore)

import json
from dataclasses import dataclass
from typing import Any

from src.config.base import getenv


# =========================
# TELEGRAM
# =========================

@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str
    webhook_url: str


# =========================
# GEMINI (legacy optional)
# =========================

@dataclass
class GeminiConfig:
    api_key: str | None


# =========================
# GOOGLE (VERTEX + SERVICES)
# =========================

@dataclass
class GoogleConfig:
    service_account: dict[str, Any] | None


# =========================
# ROOT
# =========================

@dataclass
class Config:
    telegram: TelegramConfig
    gemini: GeminiConfig
    google: GoogleConfig


# =========================
# PARSER
# =========================

def _parse_json(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None

    try:
        data = json.loads(value)

        if not isinstance(data, dict):
            raise ValueError("Service account must be JSON object")

        # normalize private key (Node-style fix)
        if "private_key" in data:
            data["private_key"] = data["private_key"].replace("\\n", "\n")

        return data

    except Exception as err:
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from err


# =========================
# LOAD CONFIG
# =========================

def load_config() -> Config:
    return Config(
        telegram=TelegramConfig(
            token=getenv("TELEGRAM_TOKEN"),
            webhook_secret=getenv("WEBHOOK_SECRET"),
            webhook_url=getenv("WEBHOOK_URL"),
        ),
        gemini=GeminiConfig(
            api_key=getenv("GEMINI_API_KEY", default=None),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                getenv("GOOGLE_SERVICE_ACCOUNT", default=None)
            ),
        ),
    )