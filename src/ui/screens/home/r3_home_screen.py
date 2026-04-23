# src/ui/screens/home/r3_home_screen.py

"""
R3 Home Screen.
"""

from datetime import datetime

from src.ui.screen_contracts import ScreenContext, ScreenResult
from src.ui.keyboards.home.r3_home_kb import build_r3_home_kb


async def render_r3_home_screen(context: ScreenContext) -> ScreenResult:
    user_id = context.get("user_id", "unknown")
    role = context.get("role", "R3")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "text": (
            f"🏠 HOME SCREEN\n"
            f"User: {user_id}\n"
            f"Role: {role}\n"
            f"Time: {now}"
        ),
        "keyboard": build_r3_home_kb(),
    }