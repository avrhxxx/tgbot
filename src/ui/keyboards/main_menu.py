# =========================================
# FILE: src/ui/keyboards/main_menu.py
# DESCRIPTION:
# Main Menu inline keyboard (routing layer)
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📣 Announcements",
                    callback_data="flow:announcement"
                )
            ]
        ]
    )