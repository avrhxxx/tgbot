# =========================================
# GROUP: telegram.windows.home
# FILE: home_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import HomeSG
from src.telegram.routing.core.engine import engine


async def get_home_data(dialog_manager, **kwargs):
    user = dialog_manager.middleware_data.get("user")

    if not user:
        user = dialog_manager.event.from_user

    profile = dialog_manager.middleware_data.get("profile")

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {getattr(profile, 'nickname', None) or getattr(user, 'username', None) or getattr(user, 'first_name', None) or 'User'}\n"
            f"🎮 Role: {getattr(getattr(user, 'role', None), 'value', user.role if hasattr(user, 'role') else 'R3')}"
        )
    }


home_window = Window(
    Format("{text}"),
    state=HomeSG.main,
    getter=get_home_data,
)