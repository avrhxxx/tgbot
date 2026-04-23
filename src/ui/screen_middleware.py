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

    def add(self, middleware: ScreenMiddleware):
        logger.info(f"[MW] add {middleware.__class__.__name__}")
        self._middlewares.append(middleware)

    async def run_before(self, screen_id: str, context: ScreenContext) -> ScreenContext:
        for mw in self._middlewares:
            context = await mw.before_render(screen_id, context)
        return context

    async def run_after(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult
    ) -> ScreenResult:

        for mw in self._middlewares:
            result = await mw.after_render(screen_id, context, result)

        return result


# OPTIONAL DEFAULTS

class InjectUserMiddleware:
    async def before_render(self, screen_id, context):
        if "user_id" not in context and "callback" in context:
            context["user_id"] = str(context["callback"].from_user.id)
        return context

    async def after_render(self, screen_id, context, result):
        return result