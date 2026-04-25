# =========================================
# GROUP: telegram.windows.home
# FILE: home_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HomeSG

from src.telegram.windows.home.home import get_home_data
from src.telegram.components.home_buttons import build_home_buttons
from src.telegram.routing.core.engine import engine


async def _get_data(dialog_manager, **kwargs):
    user = dialog_manager.middleware_data["user"]

    profile = dialog_manager.middleware_data.get("profile")

    routes = engine.resolve_available_routes(user)
    buttons = build_home_buttons(routes)

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {profile.nickname if profile and profile.nickname else 'User'}\n"
            f"🎮 Role: {user.role.value if hasattr(user.role, 'value') else user.role}"
        ),
        "buttons": buttons,
    }


home_window = Window(
    Format("{text}"),
    Row(
        Button("🏠 Home", id="home"),
        Button("🎮 Events", id="events"),
    ),
    Row(
        Button("⚙️ Settings", id="settings"),
        Button("❓ Help", id="help"),
    ),
    state=HomeSG.main,
    getter=_get_data,
)