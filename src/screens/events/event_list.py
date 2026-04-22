from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.keyboards.keyboards import back_button
from src.ui.definitions.action_ids import ActionID


def render_events_list(state, role):
    """
    EVENTS LIST SCREEN
    Pure entry point to event system (NO ACTION LOGIC)
    """

    text = (
        "📡 EVENTS\n\n"
        f"Role: {role}\n\n"
        "Browse available events or return to home."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 View Events",
                    callback_data=ActionID.GO_EVENTS
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