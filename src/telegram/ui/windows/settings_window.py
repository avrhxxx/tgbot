# =========================================
# GROUP: telegram.ui.windows
# FILE: settings_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button

from src.telegram.states.home import SettingsSG
from src.telegram.ui.controller.ui_controller import ui_controller


async def get_settings_data(dialog_manager, **kwargs):
    profile = dialog_manager.middleware_data.get("profile")
    user = dialog_manager.event.from_user

    username = (
        getattr(profile, "nickname", None)
        or getattr(user, "username", None)
        or getattr(user, "first_name", None)
        or "User"
    )

    role = getattr(getattr(profile, "role", None), "value", "R3")

    return {
        "text": f"⚙️ SETTINGS\n\n👤 Nick: {username}\n🎮 Role: {role}"
    }


settings_window = Window(
    Format("{text}"),

    Button(
        "⬅ Back",
        id="back",
        on_click=lambda c, b, m: ui_controller.switch("home", m)
    ),

    state=SettingsSG.main,
    getter=get_settings_data,
)