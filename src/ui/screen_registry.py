# src/ui/screen_registry.py
from typing import Dict, Callable, Protocol, Any


class Screen(Protocol):
    def __call__(self, **context: Any) -> dict: ...


class ScreenRegistry:
    """
    Central screen storage with contract enforcement layer.
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