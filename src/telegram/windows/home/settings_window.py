# =========================================
# GROUP: telegram.windows.home
# FILE: settings_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import SettingsSG


async def get_settings_data(dialog_manager, **kwargs):
    user = dialog_manager.middleware_data["user"]
    profile = dialog_manager.middleware_data.get("profile")

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 Nick: {profile.nickname if profile and profile.nickname else 'User'}\n"
            f"🎮 Role: {user.role.value if hasattr(user.role, 'value') else user.role}"
        )
    }


settings_window = Window(
    Format("{text}"),
    state=SettingsSG.main,
    getter=get_settings_data,
)