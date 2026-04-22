from typing import Callable, Dict, Any

from src.screens.home.r3_home import render_home_r3
from src.screens.home.r4_home import render_home_r4
from src.screens.home.r5_home import render_home_r5

from src.screens.events.event_list import render_events_list
from src.screens.settings.settings_main import render_settings_main


ScreenRenderer = Callable[[Any], dict]


# =========================
# 🧠 SCREEN REGISTRY (UI LAYER)
# =========================
SCREEN_RENDERERS: Dict[str, ScreenRenderer] = {
    # HOME
    "home_r3": render_home_r3,
    "home_r4": render_home_r4,
    "home_r5": render_home_r5,

    # EVENTS
    "events_list": render_events_list,

    # SETTINGS
    "settings_main": render_settings_main,
}


# =========================
# 🧭 RESOLVER
# =========================
def resolve_screen(screen_id: str, state=None):
    renderer = SCREEN_RENDERERS.get(screen_id)

    if renderer:
        return renderer(state)

    # fallback tylko diagnostyczny (NIE UI placeholder)
    return {
        "text": f"Unknown screen: {screen_id}",
        "keyboard": None,
    }