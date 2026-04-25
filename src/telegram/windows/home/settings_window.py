# =========================================
# GROUP: telegram.windows.home
# FILE: settings_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import SettingsSG


def safe_user(dialog_manager):
    user = dialog_manager.middleware_data.get("user")
    if user:
        return user
    return getattr(dialog_manager.event, "from_user", None)


async def get_settings_data(dialog_manager, **kwargs):
    user = safe_user(dialog_manager)
    profile = dialog_manager.middleware_data.get("profile")

    username = (
        getattr(profile, "nickname", None)
        or getattr(user, "username", None)
        or getattr(user, "first_name", None)
        or "User"
    )

    role = getattr(getattr(user, "role", None), "value", "R3")

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 Nick: {username}\n"
            f"🎮 Role: {role}"
        )
    }


settings_window = Window(
    Format("{text}"),
    state=SettingsSG.main,
    getter=get_settings_data,
)