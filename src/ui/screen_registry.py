# src/ui/screen_registry.py

from typing import Dict, Callable

Screen = Callable[..., dict]


class ScreenRegistry:
    """
    Stores all screens in the system.
    Each screen returns:
    {
        "text": str,
        "keyboard": InlineKeyboardMarkup
    }
    """

    def __init__(self):
        self._screens: Dict[str, Screen] = {}

    def register(self, screen_id: str, screen_fn: Screen):
        self._screens[screen_id] = screen_fn

    def get(self, screen_id: str) -> Screen:
        if screen_id not in self._screens:
            raise ValueError(f"Screen not found: {screen_id}")
        return self._screens[screen_id]

    def render(self, screen_id: str, **context) -> dict:
        screen = self.get(screen_id)
        return screen(**context)