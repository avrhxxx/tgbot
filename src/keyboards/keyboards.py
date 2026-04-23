from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.role_cycle import get_next_role
from config.config import load_config

from src.ui.callbacks.navigation import NavigationCB
from src.ui.callbacks.event import EventCB
from src.ui.callbacks.role import RoleCB


# =========================
# 🧭 GLOBAL NAVIGATION KEYS
# =========================

def back_button():
    return InlineKeyboardButton(
        text="⬅️ Back",
        callback_data=NavigationCB(target="back").pack()
    )


def home_button():
    return InlineKeyboardButton(
        text="🏠 Home",
        callback_data=NavigationCB(target="home").pack()
    )


# =========================
# 🎭 ROLE SWITCH BUTTON
# =========================

def switch_role_button(role: str):
    next_role = get_next_role(role)

    return InlineKeyboardButton(
        text=f"🎭 Switch Role ({role} → {next_role})",
        callback_data=RoleCB(action="switch").pack()
    )


# =========================
# 🔥 CONFIG
# =========================

def is_demo_mode_enabled() -> bool:
    config = load_config()
    return config.features.demo_mode


# =========================
# 🏠 HOME KEYBOARD
# =========================

def home_keyboard(role: str):
    rows = []

    # BASE LAYOUT
    rows.append([
        InlineKeyboardButton(
            text="📅 Events",
            callback_data=NavigationCB(target="events").pack()
        ),
        InlineKeyboardButton(
            text="⚡ Quick Join",
            callback_data=EventCB(action="join").pack()
        )
    ])

    # SETTINGS
    rows.append([
        InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data=NavigationCB(target="settings").pack()
        ),
        InlineKeyboardButton(
            text="❓ Help",
            callback_data=NavigationCB(target="home").pack()
        )
    ])

    # =========================
    # 🎭 ROLE SWITCH (ONLY DEMO MODE)
    # =========================
    if is_demo_mode_enabled():
        rows.append([
            switch_role_button(role)
        ])

    # =========================
    # 🧭 R4+ FEATURES
    # =========================
    if role in ("R4", "R5", "ADMIN"):
        rows.append([
            InlineKeyboardButton(
                text="🧭 Event Management",
                callback_data=NavigationCB(target="event_management").pack()
            )
        ])

    # =========================
    # 👥 R5+ FEATURES
    # =========================
    if role in ("R5", "ADMIN"):
        rows.append([
            InlineKeyboardButton(
                text="👥 User Management",
                callback_data=NavigationCB(target="home").pack()
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