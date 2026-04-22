from aiogram.types import InlineKeyboardMarkup

from src.keyboards.keyboards import back_button


def render_settings_main(state, role):
    """
    SETTINGS SCREEN (placeholder v1)
    """

    text = (
        "⚙️ SETTINGS\n\n"
        f"Role: {role}\n\n"
        "No settings available yet.\n"
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