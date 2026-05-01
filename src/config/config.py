# src/config/config.py
# GROUP: config
# DESCRIPTION: MVP config for AI Wiki Bot (Telegram + Gemini + Firestore)

import json
from dataclasses import dataclass

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
# GEMINI
# =========================

@dataclass
class GeminiConfig:
    api_key: str


# =========================
# GOOGLE / FIRESTORE
# =========================

@dataclass
class GoogleConfig:
    service_account: str | None


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

def _parse_json(value: str | None):
    if not value:
        return None

    try:
        return json.loads(value)

    except Exception as err:
        raise ValueError("Invalid JSON in environment variable") from err


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
            api_key=getenv("GEMINI_API_KEY"),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                getenv("GOOGLE_SERVICE_ACCOUNT", default=None)
            ),
        ),
    )