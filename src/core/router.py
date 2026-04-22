from typing import Callable, Dict, Any

from config.config import load_config

from src.core.role_resolver import resolve_role
from src.ui.definitions.screen_ids import ScreenID

from src.screens.home.home import render_home
from src.screens.events.event_list import render_events_list
from src.screens.settings.settings_main import render_settings_main


ScreenRenderer = Callable[[Any, str], dict]


# =========================
# 🧠 SCREEN REGISTRY (NEW ARCHITECTURE)
# =========================
SCREEN_RENDERERS: Dict[str, ScreenRenderer] = {
    "home": render_home,

    ScreenID.EVENTS_LIST: render_events_list,
    ScreenID.SETTINGS_MAIN: render_settings_main,
}


# =========================
# 🧭 RESOLVER
# =========================
def resolve_screen(screen_id: str, state=None):
    """
    Final UI composition layer:
    state → role context → renderer → payload
    """

    config = load_config()

    renderer = SCREEN_RENDERERS.get(screen_id)

    if not renderer:
        return {
            "text": f"⚠️ Unknown screen: {screen_id}",
            "keyboard": None,
        }

    if not state:
        return {
            "text": "⚠️ Missing state",
            "keyboard": None,
        }

    # =========================
    # 🎭 ROLE RESOLUTION (SINGLE SOURCE OF TRUTH)
    # =========================
    role_ctx = resolve_role(state.user_id, state.role)
    effective_role = role_ctx.effective_role

    # =========================
    # 🧠 RENDER SCREEN
    # =========================
    payload = renderer(state, effective_role)

    return payload