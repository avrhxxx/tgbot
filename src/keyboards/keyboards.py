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
        callback_data="back"
    )


def home_button():
    return InlineKeyboardButton(
        text="🏠 Home",
        callback_data="go_home"
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
        callback_data=f"demo_switch_role:{next_role}"
    )


# =========================
# 🏠 HOME KEYBOARD
# =========================

def home_keyboard(user_id: int = None):
    keyboard = [
        [
            InlineKeyboardButton(
                text="📡 Events",
                callback_data="go_events"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Settings",
                callback_data="go_settings"
            )
        ]
    ]

    # =========================
    # DEMO MODE GATE
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