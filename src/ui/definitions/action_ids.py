class ActionID:
    """
    SINGLE SOURCE OF TRUTH for all UI callback actions.
    """

    # NAVIGATION
    GO_HOME = "go_home"
    GO_EVENTS = "go_events"
    GO_SETTINGS = "go_settings"
    BACK = "back"

    # EVENTS
    OPEN_EVENT = "open_event"
    JOIN_EVENT = "join_event"
    LEAVE_EVENT = "leave_event"

    # EVENT MANAGEMENT
    GO_EVENT_MANAGEMENT = "go_event_management"
    CREATE_EVENT = "create_event"

    # SETTINGS
    CHANGE_GAME_NICK = "change_game_nick"

    # ROLE SYSTEM
    SWITCH_ROLE = "switch_role"