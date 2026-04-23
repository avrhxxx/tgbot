# src/ui/keyboards/home/r3_home_kb.py

"""
R3 Home screen keyboard.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_r3_home_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Events",
                    callback_data="nav:events",
                ),
                InlineKeyboardButton(
                    text="⚡ Quick Join",
                    callback_data="nav:quick_join",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Settings",
                    callback_data="nav:settings",
                ),
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="nav:help",
                ),
            ],
        ]
    )