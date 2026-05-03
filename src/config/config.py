# src/config/config.py
# GROUP: config
# DESCRIPTION: Central runtime config (Railway-safe, single source of truth)

import json
import logging
from dataclasses import dataclass
from typing import Any

from src.config.base import getenv

logger = logging.getLogger("config")


# =========================
# TELEGRAM
# =========================

@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str
    webhook_url: str
    admin_ids: list[int]


# =========================
# GEMINI (AI LAYER)
# =========================

@dataclass
class GeminiConfig:
    api_key: str | None


# =========================
# GOOGLE SHEETS + AUTH
# =========================

@dataclass
class GoogleConfig:
    service_account: dict[str, Any] | None
    sheets_id: str | None


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

def _parse_json(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None

    try:
        data = json.loads(value)

        if not isinstance(data, dict):
            raise ValueError("Expected JSON object")

        # fix private key formatting for Google SA
        if "private_key" in data:
            data["private_key"] = data["private_key"].replace("\\n", "\n")

        return data

    except Exception as err:
        logger.error("❌ GOOGLE_SERVICE_ACCOUNT parse failed: %s", err)
        return None


def _parse_admin_ids(value: str | None) -> list[int]:
    if not value:
        return []

    try:
        return [int(x.strip()) for x in value.split(",") if x.strip()]
    except Exception:
        logger.error("❌ ADMIN_IDS parse failed")
        return []


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
            admin_ids=_parse_admin_ids(getenv("ADMIN_IDS")),
        ),
        gemini=GeminiConfig(
            api_key=getenv("GEMINI_API_KEY", required=False),
        ),
        google=GoogleConfig(
            service_account=_parse_json(
                getenv("GOOGLE_SERVICE_ACCOUNT", required=False)
            ),
            sheets_id=getenv("GOOGLE_SHEET_ID", required=False),
        ),
    )

    logger.info(
        "✅ Config loaded | sheets=%s | gemini=%s | admins=%s",
        bool(cfg.google.sheets_id),
        bool(cfg.gemini.api_key),
        len(cfg.telegram.admin_ids),
    )

    return cfg