# src/ui/screen_middleware.py

"""
Middleware pipeline for screen rendering system.
"""

import logging
from typing import Any, Dict, List, Protocol

logger = logging.getLogger("shadow.ui.middleware")


ScreenContext = Dict[str, Any]
ScreenResult = Dict[str, Any]


class ScreenMiddleware(Protocol):
    async def before_render(
        self,
        screen_id: str,
        context: ScreenContext,
    ) -> ScreenContext:
        ...

    async def after_render(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult,
    ) -> ScreenResult:
        ...


class ScreenMiddlewareManager:
    def __init__(self):
        self._middlewares: List[ScreenMiddleware] = []

    def add(self, middleware: ScreenMiddleware) -> None:
        logger.info(f"[MW] add {middleware.__class__.__name__}")
        self._middlewares.append(middleware)

    async def run_before(
        self,
        screen_id: str,
        context: ScreenContext,
    ) -> ScreenContext:
        for mw in self._middlewares:
            context = await mw.before_render(screen_id, context)
        return context

    async def run_after(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult,
    ) -> ScreenResult:
        for mw in self._middlewares:
            result = await mw.after_render(screen_id, context, result)
        return result


# =========================
# FIXED MIDDLEWARE
# =========================
class InjectUserMiddleware:
    """
    SAFE VERSION:
    - no assumption about callback presence
    """

    async def before_render(self, screen_id, context):
        if "user_id" not in context:
            callback = context.get("callback")
            if callback:
                context["user_id"] = str(callback.from_user.id)

        return context

    async def after_render(self, screen_id, context, result):
        return result