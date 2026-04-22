from typing import Callable, Dict, Any

from config.config import load_config
from src.core.state_store import state_store

from src.ui.definitions.screen_ids import ScreenID

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
    config = load_config()

    renderer = SCREEN_RENDERERS.get(screen_id)

    if not renderer:
        return {
            "text": f"⚠️ Unknown screen: {screen_id}",
            "keyboard": None,
        }

    payload = renderer(state)

    # =========================
    # 🎭 DEMO MODE (UI DECORATION ONLY)
    # =========================
    if config.features.demo_mode and state:
        demo_role = state_store.get_demo_role(state.user_id)

        if demo_role and str(screen_id).startswith("home_"):
            payload["text"] += f"\n\n🎭 DEMO MODE: {demo_role}"

    return payload