# =========================================
# GROUP: telegram.windows.home
# FILE: home_window.py
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import HomeSG
from src.telegram.utils.safe_context import get_user_safe


async def get_home_data(dialog_manager, **kwargs):
    user = get_user_safe(dialog_manager)
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
            "🏠 HOME\n\n"
            f"👤 Nick: {username}\n"
            f"🎮 Role: {role}"
        )
    }


home_window = Window(
    Format("{text}"),
    state=HomeSG.main,
    getter=get_home_data,
)