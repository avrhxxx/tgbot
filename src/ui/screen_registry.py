# src/ui/screen_registry.py
import logging
from typing import Dict, Protocol, Any, Callable, Awaitable

from src.ui.screen_contracts import ScreenResult, ScreenContext

logger = logging.getLogger("shadow.ui.registry")


class Screen(Protocol):
    async def __call__(self, **context: Any) -> ScreenResult:
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

    def render(self, screen_id: str, **context: Any) -> ScreenResult:
        logger.debug(f"[REGISTRY] render: {screen_id}")

        result = self.get(screen_id)(**context)

        # SAFETY CHECK
        if "text" not in result or "keyboard" not in result:
            logger.error(f"[REGISTRY] invalid screen output: {screen_id}")
            raise ValueError(f"Screen '{screen_id}' must return text + keyboard")

        return result