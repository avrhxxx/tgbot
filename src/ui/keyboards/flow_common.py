# =========================================
# FILE: src/ui/keyboards/flow_common.py
# DESCRIPTION:
# Shared navigation buttons for all flows
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="nav:main"
                )
            ]
        ]
    )