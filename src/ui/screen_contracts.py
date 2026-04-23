# src/ui/screen_contracts.py
from typing import TypedDict, Any


class ScreenResult(TypedDict):
    text: str
    keyboard: Any  # UI layer (aiogram markup is dynamic)


class ScreenContext(TypedDict, total=False):
    app: Any
    user_id: str
    callback: Any