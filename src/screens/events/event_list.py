from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.keyboards.keyboards import back_button


def render_events_list(state):
    """
    EVENTS LIST SCREEN (v1)
    Entry point for Events system
    """

    text = (
        "📡 EVENTS\n\n"
        "Choose an option below:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 View Events",
                    callback_data="events_view"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚡ Quick Join",
                    callback_data="events_quick_join"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Create Event",
                    callback_data="events_create"
                )
            ],
            [back_button()]
        ]
    )

    return {
        "text": text,
        "keyboard": keyboard
    }