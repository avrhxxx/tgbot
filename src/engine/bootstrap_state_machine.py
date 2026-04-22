from src.engine.state_machine import StateMachine
from src.ui.definitions.action_ids import ActionID
from src.ui.definitions.screen_ids import ScreenID


def build_state_machine() -> StateMachine:
    sm = StateMachine()

    # =========================
    # HOME
    # =========================
    sm.add_transition(ScreenID.HOME_R3, ActionID.GO_HOME, ScreenID.HOME_R3)
    sm.add_transition(ScreenID.HOME_R3, ActionID.GO_EVENTS, ScreenID.EVENTS_LIST)
    sm.add_transition(ScreenID.HOME_R3, ActionID.GO_SETTINGS, ScreenID.SETTINGS_MAIN)
    sm.add_transition(ScreenID.HOME_R3, ActionID.BACK, ScreenID.HOME_R3)

    # =========================
    # EVENTS
    # =========================
    sm.add_transition(ScreenID.EVENTS_LIST, ActionID.BACK, ScreenID.HOME_R3)
    sm.add_transition(ScreenID.EVENTS_LIST, ActionID.GO_HOME, ScreenID.HOME_R3)
    sm.add_transition(ScreenID.EVENTS_LIST, ActionID.GO_EVENTS, ScreenID.EVENTS_LIST)

    # =========================
    # SETTINGS
    # =========================
    sm.add_transition(ScreenID.SETTINGS_MAIN, ActionID.BACK, ScreenID.HOME_R3)
    sm.add_transition(ScreenID.SETTINGS_MAIN, ActionID.GO_HOME, ScreenID.HOME_R3)

    return sm