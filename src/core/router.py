from src.core.registry import SCREEN_MAP
from src.screens.home.r3_home import render_home_r3
from src.screens.home.r4_home import render_home_r4
from src.screens.home.r5_home import render_home_r5


def resolve_screen(screen_id: str, state=None):
    """
    Zwraca gotowy UI payload (text + keyboard)
    """

    if screen_id == "home_r3":
        return render_home_r3(state)

    if screen_id == "home_r4":
        return render_home_r4(state)

    if screen_id == "home_r5":
        return render_home_r5(state)

    if screen_id == "events_list":
        return {
            "text": "📡 Events list",
            "keyboard": None
        }

    if screen_id == "settings_main":
        return {
            "text": "⚙️ Settings",
            "keyboard": None
        }

    # fallback
    return {
        "text": f"Unknown screen: {screen_id}",
        "keyboard": None
    }