from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ui.definitions.action_ids import ActionID
from src.core.role_cycle import get_next_role
from config.config import load_config


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
# 🎭 ROLE SWITCH BUTTON (CORE FEATURE)
# =========================

def switch_role_button(role: str):
    next_role = get_next_role(role)

    return InlineKeyboardButton(
        text=f"🎭 Switch Role ({role} → {next_role})",
        callback_data=ActionID.SWITCH_ROLE
    )


def is_demo_mode_enabled() -> bool:
    config = load_config()
    return bool(getattr(config, "demo_mode", False))


# =========================
# 🏠 HOME KEYBOARD
# =========================

def home_keyboard(role: str):
    rows = []

    # =========================
    # BASE LAYOUT
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
    # 🧭 ROLE SWITCH (ONLY DEMO MODE)
    # =========================
    if is_demo_mode_enabled():
        rows.insert(1, [
            switch_role_button(role)
        ])

    # =========================
    # 🧭 R4+ FEATURES
    # =========================
    if role in ("R4", "R5", "ADMIN"):
        rows.insert(2, [
            InlineKeyboardButton(
                text="🧭 Event Management",
                callback_data=ActionID.GO_EVENT_MANAGEMENT
            )
        ])

    # =========================
    # 👥 R5+ FEATURES
    # =========================
    if role in ("R5", "ADMIN"):
        rows.append([
            InlineKeyboardButton(
                text="👥 User Management",
                callback_data=ActionID.GO_HOME  # TODO: replace later
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# =========================
# 📡 EVENTS KEYBOARD
# =========================

def events_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [back_button(), home_button()]
    ])


# =========================
# ⚙️ SETTINGS KEYBOARD
# =========================

def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [back_button(), home_button()]
    ])