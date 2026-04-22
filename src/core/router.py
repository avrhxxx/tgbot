from typing import Callable, Dict, Any

from config.config import load_config

from src.ui.definitions.screen_ids import ScreenID
from src.core.role_resolver import resolve_role

from src.screens.home.r3_home import render_home_r3
from src.screens.home.r4_home import render_home_r4
from src.screens.home.r5_home import render_home_r5

from src.screens.events.event_list import render_events_list
from src.screens.settings.settings_main import render_settings_main


ScreenRenderer = Callable[[Any], dict]


# =========================
# 🧠 SCREEN REGISTRY
# =========================
SCREEN_RENDERERS: Dict[ScreenID, ScreenRenderer] = {
    ScreenID.HOME_R3: render_home_r3,
    ScreenID.HOME_R4: render_home_r4,
    ScreenID.HOME_R5: render_home_r5,

    ScreenID.EVENTS_LIST: render_events_list,
    ScreenID.SETTINGS_MAIN: render_settings_main,
}


# =========================
# 🧭 RESOLVER
# =========================
def resolve_screen(screen_id: ScreenID, state=None):
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
    # 🎭 ROLE RESOLUTION (NEW ARCHITECTURE)
    # =========================
    role_ctx = resolve_role(state.user_id, state.role)
    effective_role = role_ctx.effective_role

    # =========================
    # 🧠 RENDER SCREEN
    # =========================
    payload = renderer(state, effective_role)

    # =========================
    # 🚫 NO MORE DEMO UI HACKS HERE
    # =========================
    # Demo mode is now fully handled in role_resolver + state_store
    # UI layer should NOT mutate text based on demo state

    return payload