from dataclasses import dataclass
from typing import List

from .base import getenv


# =====================================
# 🔹 TELEGRAM CONFIG
# =====================================

@dataclass
class TelegramBotConfig:
    token: str
    username: str
    webhook_url: str
    webhook_secret: str


# =====================================
# 🔹 GOOGLE CONFIG (RAW ONLY)
# =====================================

@dataclass
class GoogleConfig:
    service_account: str  # JSON string (Railway env)
    sheet_id: str


# =====================================
# 🔹 ACCESS CONTROL (RANK SYSTEM)
# =====================================

@dataclass
class AccessConfig:
    r5_ids: List[int]
    admin_ids: List[int]
    group_ids: List[int]


# =====================================
# 🔹 ROOT CONFIG
# =====================================

@dataclass
class Config:
    tg_bot: TelegramBotConfig
    google: GoogleConfig
    access: AccessConfig


# =====================================
# 🔧 HELPERS
# =====================================

def _parse_id_list(value: str | None) -> List[int]:
    """
    "1,2,3" -> [1,2,3]
    """
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]


# =====================================
# 🚀 LOAD CONFIG (RAILWAY READY)
# =====================================

def load_config() -> Config:
    return Config(
        tg_bot=TelegramBotConfig(
            token=getenv("BOT_TOKEN"),
            username=getenv("BOT_USERNAME"),
            webhook_url=getenv("WEBHOOK_URL"),
            webhook_secret=getenv("WEBHOOK_SECRET"),
        ),

        google=GoogleConfig(
            service_account=getenv("GOOGLE_SERVICE_ACCOUNT"),
            sheet_id=getenv("GOOGLE_SHEET_ID"),
        ),

        access=AccessConfig(
            r5_ids=_parse_id_list(getenv("R5_IDS")),
            admin_ids=_parse_id_list(getenv("ADMIN_IDS")),
            group_ids=_parse_id_list(getenv("GROUP_IDS")),
        ),
    )