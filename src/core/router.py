from typing import Callable, Dict, Any

from src.screens.home.r3_home import render_home_r3
from src.screens.home.r4_home import render_home_r4
from src.screens.home.r5_home import render_home_r5


ScreenRenderer = Callable[[Any], dict]


# =========================
# 🧠 SCREEN REGISTRY (UI LAYER)
# =========================
SCREEN_RENDERERS: Dict[str, ScreenRenderer] = {
    "home_r3": render_home_r3,
    "home_r4": render_home_r4,
    "home_r5": render_home_r5,
}


def resolve_screen(screen_id: str, state=None):
    """
    UI layer:
    state → screen_id → renderer → UI payload
    """

    # =========================
    # 🏠 REGISTERED SCREENS
    # =========================
    renderer = SCREEN_RENDERERS.get(screen_id)

    if renderer:
        return renderer(state)

    # =========================
    # 📡 STATIC SCREENS (placeholdery systemowe)
    # =========================
    static_screens = {
        "events_list": {
            "text": "📡 Events list",
            "keyboard": None,
        },
        "settings_main": {
            "text": "⚙️ Settings",
            "keyboard": None,
        },
    }

    if screen_id in static_screens:
        return static_screens[screen_id]

    # =========================
    # ❌ FALLBACK
    # =========================
    return {
        "text": f"Unknown screen: {screen_id}",
        "keyboard": None,
    }