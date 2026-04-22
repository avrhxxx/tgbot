from aiogram.types import InlineKeyboardMarkup

from src.keyboards.keyboards import back_button


def render_events_list(state):
    """
    EVENTS LIST SCREEN (placeholder v1)
    """

    text = (
        "📡 EVENTS\n\n"
        "No events available yet.\n"
        "This is a placeholder screen."
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