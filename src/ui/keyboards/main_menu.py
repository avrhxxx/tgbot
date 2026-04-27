# =========================================
# FILE: src/ui/keyboards/main_menu.py
# DESCRIPTION:
# Main Menu inline keyboard (flow router hub)
# =========================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📨 Group Message",
                    callback_data="flow:group_message"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Event Manager",
                    callback_data="flow:event_manager"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Language",
                    callback_data="flow:language"
                )
            ]
        ]
    )