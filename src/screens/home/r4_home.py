from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def render_home_r4(state):
    return {
        "text": "🏠 HOME R4\n\nSelect an option:",
        "keyboard": InlineKeyboardMarkup(
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
    }