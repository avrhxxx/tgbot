# src/config/config.py
# GROUP: config
# DESCRIPTION: SAFE runtime config (Railway-ready, non-blocking bootstrap)

import json
from dataclasses import dataclass
from typing import Any, Optional

from src.config.base import getenv


# =========================
# TELEGRAM (REQUIRED)
# =========================

@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str
    webhook_url: str


# =========================
# OPTIONAL AI (LATER)
# =========================

@dataclass
class GeminiConfig:
    api_key: Optional[str]


# =========================
# OPTIONAL GOOGLE SEARCH
# =========================

@dataclass
class GoogleSearchConfig:
    api_key: Optional[str]
    cx: Optional[str]


# =========================
# OPTIONAL GOOGLE SERVICES
# =========================

@dataclass
class GoogleConfig:
    service_account: Optional[dict[str, Any]]
    search: GoogleSearchConfig


# =========================
# ROOT CONFIG
# =========================

@dataclass
class Config:
    telegram: TelegramConfig
    gemini: GeminiConfig
    google: GoogleConfig


# =========================
# HELPERS
# =========================

def _parse_json(value: Optional[str]) -> Optional[dict[str, Any]]:
    if not value:
        return None

    try:
        data = json.loads(value)

        if not isinstance(data, dict):
            raise ValueError("Invalid JSON object")

        # fix escaped newlines for service accounts
        if "private_key" in data:
            data["private_key"] = data["private_key"].replace("\\n", "\n")

        return data

    except Exception as err:
        raise ValueError("Invalid JSON in GOOGLE_SERVICE_ACCOUNT") from err


# =========================
# LOAD CONFIG (SAFE MODE)
# =========================

def load_config() -> Config:
    return Config(
        telegram=TelegramConfig(
            token=getenv("TELEGRAM_TOKEN"),
            webhook_secret=getenv("WEBHOOK_SECRET"),
            webhook_url=getenv("WEBHOOK_URL"),
        ),
        gemini=GeminiConfig(
            api_key=getenv("GEMINI_API_KEY", default=None, required=False),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                getenv("GOOGLE_SERVICE_ACCOUNT", default=None, required=False)
            ),
            search=GoogleSearchConfig(
                api_key=getenv("GOOGLE_SEARCH_API_KEY", default=None, required=False),
                cx=getenv("GOOGLE_SEARCH_CX", default=None, required=False),
            ),
        ),
    )