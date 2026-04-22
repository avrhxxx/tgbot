from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import load_config
from src.core.state_store import state_store

config = load_config()


# =========================
# 🧭 GLOBAL NAVIGATION KEYS
# =========================

def back_button():
    return InlineKeyboardButton(
        text="⬅️ Back",
        callback_data="action:back"
    )


def home_button():
    return InlineKeyboardButton(
        text="🏠 Home",
        callback_data="action:go_home"
    )


# =========================
# 🎭 DEMO SWITCH (CORE FEATURE)
# =========================

def demo_role_switch_button(user_id: int):
    """
    Cycles roles: R3 → R4 → R5 → R3
    """

    current = state_store.get_demo_role(user_id) or "R3"

    next_role_map = {
        "R3": "R4",
        "R4": "R5",
        "R5": "R3",
    }

    next_role = next_role_map.get(current, "R3")

    return InlineKeyboardButton(
        text=f"🎭 Switch Role ({current} → {next_role})",
        callback_data=f"demo:switch_role:{next_role}"
    )


# =========================
# 🧭 R4 / R5 EXTRA PANEL
# =========================

def r4_r5_extra_keyboard():
    """
    Extra admin/officer tools (ONLY R4 / R5 UI extension)
    """

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🧭 Event Management",
                callback_data="action:go_event_management"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 User Management",
                callback_data="action:go_user_management"
            )
        ]
    ])


# =========================
# 🏠 HOME KEYBOARD (BASE = R3)
# =========================

def home_keyboard(user_id: int = None):
    keyboard = [
        [
            InlineKeyboardButton(
                text="📡 Events",
                callback_data="action:go_events"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Settings",
                callback_data="action:go_settings"
            )
        ]
    ]

    # =========================
    # DEMO MODE GATE (DO NOT TOUCH)
    # =========================
    if config.features.demo_mode and user_id is not None:
        keyboard.insert(0, [
            demo_role_switch_button(user_id)
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# =========================
# 📡 EVENTS KEYBOARD
# =========================

def events_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            back_button(),
            home_button()
        ]
    ])


# =========================
# ⚙️ SETTINGS KEYBOARD
# =========================

def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            back_button(),
            home_button()
        ]
    ])