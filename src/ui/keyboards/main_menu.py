# =========================================
# FILE: src/ui/keyboards/main_menu.py
# DESCRIPTION:
# Main menu inline keyboard (static routing layer)
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Group Message",
                    callback_data="menu:group_message"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📅 Event Manager",
                    callback_data="menu:events"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Language",
                    callback_data="menu:language"
                )
            ],
        ]
    )