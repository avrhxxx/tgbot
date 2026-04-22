from src.engine.state_machine import StateMachine
from src.core.actions import Action


def build_state_machine() -> StateMachine:
    sm = StateMachine()

    # =========================
    # 🏠 HOME FLOW
    # =========================

    sm.add_transition("home_r3", Action.GO_HOME, "home_r3")

    # FIX: UI uses GO_EVENTS → must match here
    sm.add_transition("home_r3", Action.GO_EVENTS, "events_list")

    sm.add_transition("home_r3", Action.GO_SETTINGS, "settings_main")
    sm.add_transition("home_r3", Action.BACK, "home_r3")

    # =========================
    # 📡 EVENTS
    # =========================

    sm.add_transition("events_list", Action.BACK, "home_r3")
    sm.add_transition("events_list", Action.GO_HOME, "home_r3")

    # (optional future expansion)
    sm.add_transition("events_list", Action.GO_EVENTS, "events_list")

    # =========================
    # ⚙️ SETTINGS
    # =========================

    sm.add_transition("settings_main", Action.BACK, "home_r3")
    sm.add_transition("settings_main", Action.GO_HOME, "home_r3")

    return sm