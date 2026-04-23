# src/ui/screen_context.py
from typing import TypedDict, Optional, Any


class HomeScreenContext(TypedDict):
    first_name: str
    role: str
    game_nick: Optional[str]
    is_demo: bool


class EventsScreenContext(TypedDict, total=False):
    user_id: str
    app: Any


class SettingsScreenContext(TypedDict, total=False):
    user_id: str
    app: Any