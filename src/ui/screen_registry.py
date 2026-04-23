# src/ui/screen_registry.py

import logging
from typing import Dict, Callable, Protocol, Any

logger = logging.getLogger("shadow.ui.registry")


class Screen(Protocol):
    def __call__(self, **context: Any) -> dict: ...


class ScreenRegistry:
    """
    Pure screen storage layer.
    No business logic, no routing.
    """

    def __init__(self):
        self._screens: Dict[str, Screen] = {}

    def register(self, screen_id: str, screen_fn: Screen):
        logger.info(f"[REGISTRY] Register screen: {screen_id}")
        self._screens[screen_id] = screen_fn

    def render(self, screen_id: str, **context) -> dict:
        if screen_id not in self._screens:
            logger.error(f"[REGISTRY] Screen not found: {screen_id}")
            raise ValueError(f"Screen not found: {screen_id}")

        logger.debug(f"[REGISTRY] Rendering: {screen_id}")
        return self._screens[screen_id](**context)