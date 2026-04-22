from aiogram.types import InlineKeyboardMarkup

from src.keyboards.keyboards import back_button


def render_events_list(state):
    """
    EVENTS LIST SCREEN (v1)
    Entry point for Events system
    """

    text = (
        "📡 EVENTS\n\n"
        "No events available yet.\n"
        "Create or join events will appear here soon."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [back_button()]
        ]
    )

    return {
        "text": text,
        "keyboard": keyboard
    }