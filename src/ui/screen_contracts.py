# src/ui/screen_contracts.py

"""
Screen system contracts.
Defines strict UI input/output shapes.
"""

from typing import Any, TypedDict


class ScreenResult(TypedDict):
    text: str
    keyboard: Any  # aiogram InlineKeyboardMarkup / ReplyMarkup (runtime dynamic type)


class ScreenContext(TypedDict, total=False):
    app: Any
    user_id: str
    callback: Any