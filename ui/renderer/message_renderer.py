# =========================================
# GROUP: ui.renderer
# FILE: message_renderer.py
# =========================================

from src.ui.windows.home import render_home
from src.ui.windows.settings import render_settings


async def render_screen(screen: str, user_id: int):
    if screen == "home":
        return await render_home(user_id)

    if screen == "settings":
        return await render_settings(user_id)

    return ("Unknown screen", None)