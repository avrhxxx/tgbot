# src/ui/screen_router.py

import logging
from aiogram.types import CallbackQuery

logger = logging.getLogger("shadow.ui.router")


class ScreenRouter:
    """
    ONLY routing layer.
    No rendering logic.
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
        user_id = str(callback.from_user.id)

        logger.info(f"[ROUTER] {callback.data} → {screen_id}")

        # BACK SUPPORT
        if callback.data == "nav.back":
            screen_id = self.engine.pop(user_id) or "home"

        view = await self.engine.render(
            screen_id,
            app=app,
            user_id=user_id,
            callback=callback,
        )

        await callback.message.answer(
            view["text"],
            reply_markup=view["keyboard"]
        )

        await callback.answer()

        logger.info(f"[ROUTER] done {screen_id}")