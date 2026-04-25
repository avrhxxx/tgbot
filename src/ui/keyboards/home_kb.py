# =========================================
# GROUP: ui.keyboards
# FILE: home_kb.py
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def home_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏠 Home", callback_data="home"),
                InlineKeyboardButton(text="⚙️ Settings", callback_data="settings"),
            ],
            [
                InlineKeyboardButton(text="🎮 Events", callback_data="events"),
            ],
        ]
    )


def settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="home"),
            ]
        ]
    )