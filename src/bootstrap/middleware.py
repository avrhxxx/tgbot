# src/bootstrap/middleware.py

from aiogram import BaseMiddleware


class AppMiddleware(BaseMiddleware):
    """
    Injects AppContext into all handlers as:
    data["app"]
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, handler, event, data):
        # Inject global app context into handler scope
        data["app"] = self.app

        return await handler(event, data)