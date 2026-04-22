from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.state_store import state_store
from src.ui.definitions.action_ids import ActionID


# =========================
# 🧭 GLOBAL NAVIGATION KEYS
# =========================

def back_button():
    return InlineKeyboardButton(
        text="⬅️ Back",
        callback_data=ActionID.BACK
    )


def home_button():
    return InlineKeyboardButton(
        text="🏠 Home",
        callback_data=ActionID.GO_HOME
    )


# =========================
# 🎭 DEMO SWITCH (ROLE TOOL)
# =========================

def demo_role_switch_button(user_id: int):
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
# 🏠 HOME KEYBOARD (ROLE AWARE)
# =========================

def home_keyboard(user_id: int | None = None, role: str | None = None):
    """
    role = effective_role (R3 / R4 / R5 / ADMIN)
    """

    keyboard = [
        [
            InlineKeyboardButton(
                text="📅 Events",
                callback_data=ActionID.GO_EVENTS
            ),
            InlineKeyboardButton(
                text="⚡ Quick Join",
                callback_data=ActionID.JOIN_EVENT
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Settings",
                callback_data=ActionID.GO_SETTINGS
            ),
            InlineKeyboardButton(
                text="❓ Help",
                callback_data=ActionID.GO_HOME
            )
        ]
    ]

    # =========================
    # 🎭 DEMO MODE (TEMPORARY UI TOOLING)
    # =========================
    if user_id is not None:
        demo_role = state_store.get_demo_role(user_id)

        if demo_role:
            keyboard.insert(0, [
                demo_role_switch_button(user_id)
            ])

    # =========================
    # 🧠 ROLE EXTENSIONS (REAL SYSTEM)
    # =========================

    if role in ("R4", "R5", "ADMIN"):
        keyboard.insert(1, [
            InlineKeyboardButton(
                text="🧭 Event Management",
                callback_data=ActionID.GO_EVENT_MANAGEMENT
            )
        ])

    if role in ("R5", "ADMIN"):
        keyboard.insert(2, [
            InlineKeyboardButton(
                text="👥 User Management",
                callback_data=ActionID.GO_HOME
            )
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