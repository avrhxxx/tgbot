# src/ui/screen_middleware.py
# src/ui/screen_middleware.py

from typing import Callable, Dict, Any, List, Protocol


# =========================
# TYPES
# =========================
ScreenContext = Dict[str, Any]
ScreenResult = Dict[str, Any]


class ScreenMiddleware(Protocol):
    """
    Middleware hook for screen system.
    """

    async def before_render(
        self,
        screen_id: str,
        context: ScreenContext
    ) -> ScreenContext:
        ...

    async def after_render(
        self,
        screen_id: str,
        context: ScreenContext,
        result: ScreenResult
    ) -> ScreenResult:
        ...


# =========================
# MIDDLEWARE MANAGER
# =========================
class ScreenMiddlewareManager:
    """
    Runs middleware chain around screen rendering.
    """

    def __init__(self):
        self._middlewares: List[ScreenMiddleware] = []

    def add(self, middleware: ScreenMiddleware) -> None:
        self._middlewares.append(middleware)

    async def run_before(
        self,
        screen_id: str,
        context: ScreenContext
    ) -> ScreenContext:

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


# =========================
# DEFAULT MIDDLEWARE (OPTIONAL)
# =========================
class InjectAppMiddleware:
    """
    Injects `app` automatically into screen context.
    """

    async def before_render(self, screen_id, context):
        return context

    async def after_render(self, screen_id, context, result):
        return result


class InjectUserMiddleware:
    """
    Ensures user_id is always present.
    """

    async def before_render(self, screen_id, context):
        if "user_id" not in context and "callback" in context:
            context["user_id"] = str(context["callback"].from_user.id)

        return context

    async def after_render(self, screen_id, context, result):
        return result