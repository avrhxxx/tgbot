# src/ui/screen_engine.py

from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_middleware import ScreenMiddlewareManager


class ScreenEngine:
    """
    SINGLE ENTRY POINT FOR ALL SCREEN RENDERING
    """

    def __init__(self, registry: ScreenRegistry, middleware: ScreenMiddlewareManager):
        self.registry = registry
        self.middleware = middleware

    async def render(self, screen_id: str, **context):
        # 1. BEFORE MIDDLEWARE
        context = await self.middleware.run_before(screen_id, context)

        # 2. CORE RENDER
        result = self.registry.render(screen_id, **context)

        # 3. AFTER MIDDLEWARE
        result = await self.middleware.run_after(screen_id, context, result)

        return result