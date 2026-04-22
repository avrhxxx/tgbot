from src.engine.state_machine import StateMachine


def build_state_machine() -> StateMachine:
    sm = StateMachine()

    # HOME
    sm.add_transition("home_r3", "GO_HOME", "home_r3")
    sm.add_transition("home_r3", "GO_EVENTS", "events_list")
    sm.add_transition("home_r3", "GO_SETTINGS", "settings_main")
    sm.add_transition("home_r3", "BACK", "home_r3")

    # EVENTS
    sm.add_transition("events_list", "BACK", "home_r3")
    sm.add_transition("events_list", "GO_HOME", "home_r3")
    sm.add_transition("events_list", "GO_EVENTS", "events_list")

    # SETTINGS
    sm.add_transition("settings_main", "BACK", "home_r3")
    sm.add_transition("settings_main", "GO_HOME", "home_r3")

    return sm