from typing import Callable, Dict, Any

from src.screens.home.r3_home import render_home_r3
from src.screens.home.r4_home import render_home_r4
from src.screens.home.r5_home import render_home_r5


ScreenRenderer = Callable[[Any], dict]


# =========================
# 🧠 SCREEN REGISTRY (UI LAYER)
# =========================
SCREEN_RENDERERS: Dict[str, ScreenRenderer] = {
    # HOME
    "home_r3": render_home_r3,
    "home_r4": render_home_r4,
    "home_r5": render_home_r5,
}


# =========================
# 🧭 RESOLVER
# =========================
def resolve_screen(screen_id: str, state=None):
    renderer = SCREEN_RENDERERS.get(screen_id)

    if renderer:
        return renderer(state)

    # =========================
    # 📡 STATIC PLACEHOLDERS (SAFE)
    # =========================
    static_screens = {
        "events_list": {
            "text": "📡 Events list (coming soon)",
            "keyboard": None,
        },
        "settings_main": {
            "text": "⚙️ Settings (coming soon)",
            "keyboard": None,
        },
    }

    if screen_id in static_screens:
        return static_screens[screen_id]

    return {
        "text": f"Unknown screen: {screen_id}",
        "keyboard": None,
    }