
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.keyboards.keyboards import back_button


def render_events_list(state):
    """
    EVENTS LIST SCREEN
    Pure entry point to event system (NO ACTION LOGIC)
    """

    text = (
        "📡 EVENTS\n\n"
        "Browse available events or return to home."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 View Events",
                    callback_data="action:go_events"
                )
            ],
            [
                back_button()
            ]
        ]
    )

    return {
        "text": text,
        "keyboard": keyboard
    }