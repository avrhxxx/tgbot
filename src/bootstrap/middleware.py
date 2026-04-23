# src/bootstrap/middleware.py

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware


class AppMiddleware(BaseMiddleware):
    """
    Injects AppContext into all handlers as:
    data["app"]
    """

    def __init__(self, app: Any):
        self.app = app

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        # =========================
        # SAFETY CHECK (CRITICAL)
        # =========================
        if self.app is None:
            raise RuntimeError("AppContext is None in middleware")

        # =========================
        # INJECT APP CONTEXT
        # =========================
        data["app"] = self.app

        return await handler(event, data)