from src.engine.state_machine import StateMachine
from src.core.actions import Action


def build_state_machine() -> StateMachine:
    sm = StateMachine()

    # =========================
    # 🏠 HOME FLOW
    # =========================

    sm.add_transition("home_r3", Action.GO_HOME, "home_r3")
    sm.add_transition("home_r3", Action.OPEN_EVENT, "events_list")
    sm.add_transition("home_r3", Action.BACK, "home_r3")

    # =========================
    # 📡 EVENTS
    # =========================

    sm.add_transition("events_list", Action.BACK, "home_r3")

    # =========================
    # ⚙️ SETTINGS
    # =========================

    sm.add_transition("settings_main", Action.BACK, "home_r3")

    return sm