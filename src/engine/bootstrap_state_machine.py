from src.engine.state_machine import StateMachine


def build_state_machine() -> StateMachine:
    sm = StateMachine()

    # =========================
    # 🏠 HOME FLOW (START SYSTEMU)
    # =========================

    sm.add_transition("home_r3", "open_home", "home_r3")
    sm.add_transition("home_r3", "go_events", "events_list")
    sm.add_transition("home_r3", "go_settings", "settings_main")

    # fallback / debug reset
    sm.add_transition("home_r3", "reset", "home_r3")

    # =========================
    # 📡 EVENTS (placeholder pod ETAP 7)
    # =========================

    sm.add_transition("events_list", "back_home", "home_r3")

    # =========================
    # ⚙️ SETTINGS (placeholder pod ETAP 10)
    # =========================

    sm.add_transition("settings_main", "back_home", "home_r3")

    return sm