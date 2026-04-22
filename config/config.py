from dataclasses import dataclass
import json
import os

from .base import getenv


# =========================
# TELEGRAM BOT CONFIG
# =========================

@dataclass
class TelegramBotConfig:
    token: str
    username: str
    webhook_url: str
    webhook_secret: str


# =========================
# GOOGLE CONFIG
# =========================

@dataclass
class GoogleConfig:
    service_account: str  # JSON string from Railway env
    sheet_id: str


# =========================
# ACCESS CONTROL
# =========================

@dataclass
class AccessConfig:
    r5_ids: list[int]        # game leaders (R5)
    admin_ids: list[int]     # bot/system admins (separate UI)
    group_ids: list[int]     # telegram groups / supergroups


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
    """
    "123,456,789" -> [123, 456, 789]
    """
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def _parse_google_service_account(value: str) -> str:
    """
    Validates JSON early (fail fast).
    We keep it as string for Google client later.
    """
    if not value:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT is missing")

    try:
        json.loads(value)
    except Exception as e:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT is not valid JSON") from e

    return value


def _parse_bool(value: str | None) -> bool:
    """
    Railway env parser for feature flags
    """
    return str(value).lower() == "true"


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
            r5_ids=_parse_id_list(getenv("R5_IDS")),
            admin_ids=_parse_id_list(getenv("ADMIN_IDS")),
            group_ids=_parse_id_list(getenv("GROUP_IDS")),
        ),

        features=FeatureConfig(
            demo_mode=_parse_bool(getenv("DEMO_MODE"))
        ),
    )