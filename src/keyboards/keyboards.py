from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
# 🏠 HOME KEYBOARD (ROLE-AWARE ONLY)
# =========================

def home_keyboard(role: str):
    """
    role = effective_role (already resolved)
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
    # 🧠 ROLE EXTENSIONS
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