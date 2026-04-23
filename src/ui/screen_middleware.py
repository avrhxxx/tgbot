# src/ui/screen_middleware.py

import logging
from typing import Dict, Any, List, Protocol

logger = logging.getLogger("shadow.ui.middleware")


ScreenContext = Dict[str, Any]
ScreenResult = Dict[str, Any]


class ScreenMiddleware(Protocol):
    async def before_render(self, screen_id: str, context: ScreenContext) -> ScreenContext:
        ...

    async def after_render(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult
    ) -> ScreenResult:
        ...


class ScreenMiddlewareManager:

    def __init__(self):
        self._middlewares: List[ScreenMiddleware] = []

    def add(self, middleware: ScreenMiddleware) -> None:
        logger.info(f"[MIDDLEWARE] Added: {middleware.__class__.__name__}")
        self._middlewares.append(middleware)

    async def run_before(self, screen_id: str, context: ScreenContext) -> ScreenContext:
        logger.debug(f"[MIDDLEWARE] BEFORE start: {screen_id}")

        for mw in self._middlewares:
            context = await mw.before_render(screen_id, context)

        logger.debug(f"[MIDDLEWARE] BEFORE done: {screen_id}")
        return context

    async def run_after(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult
    ) -> ScreenResult:

        logger.debug(f"[MIDDLEWARE] AFTER start: {screen_id}")

        for mw in self._middlewares:
            result = await mw.after_render(screen_id, context, result)

        logger.debug(f"[MIDDLEWARE] AFTER done: {screen_id}")
        return result