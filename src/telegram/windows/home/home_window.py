# =========================================
# GROUP: telegram.windows.home
# FILE: home_window.py
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HomeSG
from src.telegram.routing.core.engine import engine
from src.telegram.components.home_buttons import build_home_buttons

logger = logging.getLogger(__name__)


async def get_home_data(dialog_manager, **kwargs):
    user = dialog_manager.middleware_data.get("user")
    profile = dialog_manager.middleware_data.get("profile")

    if not user:
        user = dialog_manager.event.from_user

    routes = engine.resolve_available_routes(user)
    buttons = build_home_buttons(routes)

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {profile.nickname if profile and profile.nickname else (user.username or user.first_name or 'User')}\n"
            f"🎮 Role: {getattr(user.role, 'value', user.role)}"
        ),
        "buttons": buttons,
    }


home_window = Window(
    Format("{text}"),
    state=HomeSG.main,
    getter=get_home_data,
)