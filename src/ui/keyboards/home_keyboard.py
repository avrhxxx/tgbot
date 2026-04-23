# src/ui/keyboards/home_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_home_keyboard(is_demo: bool) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="📅 Events", callback_data="nav.events"),
            InlineKeyboardButton(text="⚡ Quick Join", callback_data="nav.quick_join"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Settings", callback_data="nav.settings"),
            InlineKeyboardButton(text="❓ Help", callback_data="nav.help"),
        ],
    ]

    # DEMO ONLY FEATURE
    if is_demo:
        rows.append([
            InlineKeyboardButton(
                text="🔁 Switch Role (Demo only)",
                callback_data="demo.switch_role"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)