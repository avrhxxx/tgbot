# src/config/config.py
# DESCRIPTION:
# Clean MVP config for moderator broadcast bot.
# Maps environment variables into structured dataclasses.

from dataclasses import dataclass
import json

from .base import getenv


# =========================
# BOT CONFIG
# =========================

@dataclass
class TelegramBotConfig:
    token: str
    username: str
    webhook_url: str
    webhook_secret: str


# =========================
# GOOGLE CONFIG (OPTIONAL)
# =========================

@dataclass
class GoogleConfig:
    service_account: str
    sheet_id: str


# =========================
# ACCESS CONTROL (MVP)
# =========================

@dataclass
class AccessConfig:
    admin_ids: list[int]
    mod_ids: list[int]
    chat_ids: list[int]


# =========================
# FEATURE FLAGS
# =========================

@dataclass
class FeatureConfig:
    demo_mode: bool


# =========================
# ROOT CONFIG
# =========================

@dataclass
class Config:
    tg_bot: TelegramBotConfig
    google: GoogleConfig
    access: AccessConfig
    features: FeatureConfig


# =========================
# HELPERS
# =========================

def _parse_id_list(value: str | None) -> list[int]:
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def _parse_google_service_account(value: str | None) -> str:
    if not value:
        return ""

    try:
        json.loads(value)
    except Exception as e:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT is not valid JSON") from e

    return value


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default

    value = str(value).strip().lower()

    return value in ("true", "1", "yes", "y", "on")


# =========================
# LOAD CONFIG
# =========================

def load_config() -> Config:
    return Config(
        tg_bot=TelegramBotConfig(
            token=getenv("BOT_TOKEN"),
            username=getenv("BOT_USERNAME"),
            webhook_url=getenv("WEBHOOK_URL"),
            webhook_secret=getenv("WEBHOOK_SECRET"),
        ),
        google=GoogleConfig(
            service_account=_parse_google_service_account(
                getenv("GOOGLE_SERVICE_ACCOUNT")
            ),
            sheet_id=getenv("GOOGLE_SHEET_ID"),
        ),
        access=AccessConfig(
            admin_ids=_parse_id_list(getenv("ADMIN_IDS")),
            mod_ids=_parse_id_list(getenv("MODS_IDS")),
            chat_ids=_parse_id_list(getenv("CHAT_IDS")),
        ),
        features=FeatureConfig(
            demo_mode=_parse_bool(getenv("DEMO_MODE"))
        ),
    )