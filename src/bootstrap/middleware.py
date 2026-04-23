# src/bootstrap/middleware.py

from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class AppMiddleware(BaseMiddleware):
    """
    Injects AppContext into all handlers as:
    data["app"]
    """

    def __init__(self, app):
        self.app = app

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
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