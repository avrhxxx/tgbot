# src/ui/screen_contracts.py
from typing import TypedDict, Any, Protocol


class ScreenResult(TypedDict):
    text: str
    keyboard: Any


class ScreenContext(TypedDict, total=False):
    app: object
    user_id: str
    callback: object