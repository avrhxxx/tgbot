# src/config/config.py
# GROUP: config
# DESCRIPTION: SAFE runtime config (Railway-ready, non-blocking bootstrap)

import json
import logging
from dataclasses import dataclass
from typing import Any, Optional

from src.config.base import getenv

logger = logging.getLogger("config")


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
    sheets_id: Optional[str]   # 🔥 FIX ADDED


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

        if "private_key" in data:
            data["private_key"] = data["private_key"].replace("\\n", "\n")

        return data

    except Exception as err:
        logger.error("❌ GOOGLE_SERVICE_ACCOUNT parse failed: %s", err)
        raise ValueError("Invalid JSON in GOOGLE_SERVICE_ACCOUNT") from err


# =========================
# LOAD CONFIG
# =========================

def load_config() -> Config:
    logger.info("⚙️ Loading runtime config...")

    cfg = Config(
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
            sheets_id=getenv("GOOGLE_SHEET_ID", default=None, required=False),  # 🔥 FIX
        ),
    )

    logger.info(
        "✅ Config loaded | sheets=%s | gemini=%s | search=%s",
        bool(cfg.google.sheets_id),
        bool(cfg.gemini.api_key),
        bool(cfg.google.search.api_key),
    )

    return cfg