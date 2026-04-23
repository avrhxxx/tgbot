# src/ui/screen_registry.py

import logging
from typing import Dict, Protocol, Any, Awaitable

from src.ui.screen_contracts import ScreenResult, ScreenContext

logger = logging.getLogger("shadow.ui.registry")


class Screen(Protocol):
    """
    Strict screen contract used by ScreenRegistry.
    """

    def __call__(self, context: ScreenContext) -> Awaitable[ScreenResult]:
        """
        Async screen callable contract.
        Must return ScreenResult.
        """
        ...


class ScreenRegistry:
    """
    Pure registry - no logic, no routing.
    """

    def __init__(self):
        self._screens: Dict[str, Screen] = {}

    def register(self, screen_id: str, screen_fn: Screen) -> None:
        logger.info(f"[REGISTRY] register screen: {screen_id}")
        self._screens[screen_id] = screen_fn

    def get(self, screen_id: str) -> Screen:
        if screen_id not in self._screens:
            logger.error(f"[REGISTRY] missing screen: {screen_id}")
            raise ValueError(f"Screen not found: {screen_id}")
        return self._screens[screen_id]

    async def render(self, screen_id: str, context: ScreenContext) -> ScreenResult:
        logger.debug(f"[REGISTRY] render: {screen_id}")

        screen = self.get(screen_id)
        result = await screen(context)

        if not isinstance(result, dict):
            logger.error(f"[REGISTRY] invalid screen output type: {screen_id}")
            raise ValueError(f"Screen '{screen_id}' must return dict")

        if "text" not in result or "keyboard" not in result:
            logger.error(f"[REGISTRY] invalid screen output: {screen_id}")
            raise ValueError(f"Screen '{screen_id}' must return text + keyboard")

        return result