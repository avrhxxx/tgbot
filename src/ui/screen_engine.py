# src/ui/screen_engine.py

import logging
from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_middleware import ScreenMiddlewareManager

logger = logging.getLogger("shadow.ui.screen_engine")


class ScreenEngine:
    """
    Single entry point for rendering screens.
    Handles middleware + logging + registry execution.
    """

    def __init__(self, registry: ScreenRegistry, middleware: ScreenMiddlewareManager):
        self.registry = registry
        self.middleware = middleware

    async def render(self, screen_id: str, **context):
        logger.info(f"[SCREEN ENGINE] Start render: {screen_id}")
        logger.debug(f"[SCREEN ENGINE] Context: {context}")

        # BEFORE MIDDLEWARE
        logger.debug(f"[SCREEN ENGINE] Running before middleware: {screen_id}")
        context = await self.middleware.run_before(screen_id, context)

        # CORE RENDER
        logger.info(f"[SCREEN ENGINE] Rendering screen: {screen_id}")
        result = self.registry.render(screen_id, **context)

        # AFTER MIDDLEWARE
        logger.debug(f"[SCREEN ENGINE] Running after middleware: {screen_id}")
        result = await self.middleware.run_after(screen_id, context, result)

        logger.info(f"[SCREEN ENGINE] Render complete: {screen_id}")
        return result