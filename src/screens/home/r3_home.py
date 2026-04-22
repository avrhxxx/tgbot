from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def render_home_r3(state):
    """
    UI dla HOME R3
    """

    text = (
        "🏠 HOME R3\n\n"
        "Wybierz opcję:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📡 Events",
                    callback_data="go_events"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Settings",
                    callback_data="go_settings"
                )
            ]
        ]
    )

    return {
        "text": text,
        "keyboard": keyboard
    }