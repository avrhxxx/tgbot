# =========================================
# FILE: src/ui/keyboards/group_message.py
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def group_message_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="nav:back"
                )
            ]
        ]
    )