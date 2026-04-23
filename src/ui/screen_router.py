# src/ui/screen_router.py

import logging
from aiogram.types import CallbackQuery

logger = logging.getLogger("shadow.ui.screen_router")


class ScreenRouter:
    """
    Only resolves callback → delegates to ScreenEngine.
    """

    def __init__(self, engine):
        self.engine = engine

    def resolve(self, callback_data: str) -> str:
        if callback_data.startswith("nav."):
            return callback_data.replace("nav.", "")

        if callback_data.startswith("screen:"):
            return callback_data.split(":")[1]

        return callback_data

    async def handle(self, callback: CallbackQuery, app):
        screen_id = self.resolve(callback.data)

        logger.info(f"[ROUTER] Callback received: {callback.data}")
        logger.info(f"[ROUTER] Resolved screen: {screen_id}")

        view = await self.engine.render(
            screen_id,
            app=app,
            user_id=str(callback.from_user.id),
            callback=callback,
        )

        await callback.message.answer(
            view["text"],
            reply_markup=view["keyboard"]
        )

        await callback.answer()

        logger.info(f"[ROUTER] Response sent for: {screen_id}")