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
# 🏠 HOME KEYBOARD (STABLE ROLE-AWARE VERSION)
# =========================

def home_keyboard(role: str):
    """
    role = effective_role (already resolved upstream)
    deterministic layout, no insert() mutations
    """

    rows = []

    # =========================
    # BASE LAYOUT (EVERYONE)
    # =========================
    rows.append([
        InlineKeyboardButton(
            text="📅 Events",
            callback_data=ActionID.GO_EVENTS
        ),
        InlineKeyboardButton(
            text="⚡ Quick Join",
            callback_data=ActionID.JOIN_EVENT
        )
    ])

    # =========================
    # SETTINGS ROW (EVERYONE)
    # =========================
    rows.append([
        InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data=ActionID.GO_SETTINGS
        ),
        InlineKeyboardButton(
            text="❓ Help",
            callback_data=ActionID.GO_HOME
        )
    ])

    # =========================
    # 🧭 R4+ FEATURE LAYER
    # =========================
    if role in ("R4", "R5", "ADMIN"):
        rows.insert(1, [
            InlineKeyboardButton(
                text="🧭 Event Management",
                callback_data=ActionID.GO_EVENT_MANAGEMENT
            )
        ])

    # =========================
    # 👥 R5+ FEATURE LAYER
    # =========================
    if role in ("R5", "ADMIN"):
        rows.append([
            InlineKeyboardButton(
                text="👥 User Management",
                callback_data=ActionID.GO_HOME  # placeholder for future action
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


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