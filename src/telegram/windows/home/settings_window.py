# =========================================
# GROUP: telegram.windows.home
# FILE: settings_window.py
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import SettingsSG

logger = logging.getLogger(__name__)


async def get_settings_data(dialog_manager, **kwargs):
    user = dialog_manager.middleware_data.get("user")

    if not user:
        user = dialog_manager.event.from_user

    profile = dialog_manager.middleware_data.get("profile")

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 Nick: {getattr(profile, 'nickname', None) or user.username or user.first_name or 'User'}\n"
            f"🎮 Role: {getattr(user.role, 'value', user.role)}"
        )
    }


settings_window = Window(
    Format("{text}"),
    state=SettingsSG.main,
    getter=get_settings_data,
)