from enum import Enum


class Action(str, Enum):
    # =========================
    # 🧭 NAVIGATION (HOME / UI)
    # =========================
    GO_HOME = "action:go_home"
    GO_EVENTS = "action:go_events"
    GO_SETTINGS = "action:go_settings"
    BACK = "action:back"

    # =========================
    # 📡 EVENTS (ENTRY LEVEL)
    # =========================
    OPEN_EVENT = "action:open_event"
    JOIN_EVENT = "action:join_event"
    LEAVE_EVENT = "action:leave_event"

    # =========================
    # 🧠 EVENT MANAGEMENT (R4/R5)
    # =========================
    GO_EVENT_MANAGEMENT = "action:go_event_management"
    CREATE_EVENT = "action:create_event"
    OPEN_EVENT_MANAGE = "action:open_event_manage"

    # =========================
    # ⚙️ SETTINGS
    # =========================
    OPEN_SETTINGS = "action:open_settings"
    CHANGE_GAME_NICK = "action:change_game_nick"

    # =========================
    # 🧪 SYSTEM / DEMO
    # =========================
    DEMO_SWITCH_ROLE = "demo:switch_role"