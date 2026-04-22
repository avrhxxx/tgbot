from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
# 🏠 HOME KEYBOARD
# =========================

def home_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
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
    ])


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