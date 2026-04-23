# src/ui/screen_registry.py

import logging
from typing import Dict, Callable, Any, Protocol

logger = logging.getLogger("shadow.ui.registry")


class Screen(Protocol):
    def __call__(self, **context: Any) -> dict:
        ...


class ScreenRegistry:
    """
    Pure registry - no logic, no routing.
    """

    def __init__(self):
        self._screens: Dict[str, Screen] = {}

    def register(self, screen_id: str, screen_fn: Screen):
        logger.info(f"[REGISTRY] register screen: {screen_id}")
        self._screens[screen_id] = screen_fn

    def get(self, screen_id: str) -> Screen:
        if screen_id not in self._screens:
            logger.error(f"[REGISTRY] missing screen: {screen_id}")
            raise ValueError(f"Screen not found: {screen_id}")
        return self._screens[screen_id]

    def render(self, screen_id: str, **context) -> dict:
        logger.debug(f"[REGISTRY] render: {screen_id}")
        return self.get(screen_id)(**context)