# =========================================
# GROUP: telegram.ui.windows
# FILE: home_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row

from src.telegram.states.home import HomeSG
from src.telegram.ui.controller.ui_controller import ui_controller


async def get_home_data(dialog_manager, **kwargs):
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
        "text": f"🏠 HOME\n\n👤 Nick: {username}\n🎮 Role: {role}"
    }


home_window = Window(
    Format("{text}"),

    Row(
        Button("🏠 Home", id="home",
               on_click=lambda c, b, m: ui_controller.switch("home", m)),
        Button("🎮 Events", id="events",
               on_click=lambda c, b, m: ui_controller.switch("events", m)),
    ),

    Row(
        Button("⚙️ Settings", id="settings",
               on_click=lambda c, b, m: ui_controller.switch("settings", m)),
        Button("❓ Help", id="help",
               on_click=lambda c, b, m: ui_controller.switch("help", m)),
    ),

    state=HomeSG.main,
    getter=get_home_data,
)