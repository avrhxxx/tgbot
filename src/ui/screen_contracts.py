# src/ui/screen_contracts.py
from typing import TypedDict, Any


class ScreenResult(TypedDict):
    text: str
    keyboard: Any  # aiogram InlineKeyboardMarkup / ReplyMarkup (dynamic type in runtime)


class ScreenContext(TypedDict, total=False):
    app: Any
    user_id: str
    callback: Any