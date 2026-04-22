from typing import Callable, Dict, Any

from config.config import load_config
from src.core.state_store import state_store

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
    "events": render_events_list,

    # SETTINGS
    "settings": render_settings_main,
}


# =========================
# 🧭 RESOLVER
# =========================
def resolve_screen(screen_id: str, state=None):
    config = load_config()

    # =========================
    # 🎭 DEMO MODE OVERRIDE
    # =========================
    if config.features.demo_mode and state:
        demo_role = state_store.get_demo_role(state.user_id)

        # override only HOME screens
        if demo_role and screen_id.startswith("home_"):
            screen_id = f"home_{demo_role.lower()}"

    renderer = SCREEN_RENDERERS.get(screen_id)

    if renderer:
        return renderer(state)

    # fallback only for debugging
    return {
        "text": f"Unknown screen: {screen_id}",
        "keyboard": None,
    }