# src/ui/screen_router.py

import logging
from aiogram.types import CallbackQuery, Message, InaccessibleMessage

logger = logging.getLogger("shadow.ui.router")


class ScreenRouter:
    """
    ONLY routing layer.
    No rendering logic.
    """

    def __init__(self, engine):
        self.engine = engine

    def resolve(self, callback_data: str) -> str:
        if not callback_data:
            return "home"

        if callback_data.startswith("nav."):
            return callback_data.replace("nav.", "")

        if callback_data.startswith("screen:"):
            parts = callback_data.split(":")
            return parts[1] if len(parts) > 1 else "home"

        return callback_data

    async def handle(self, callback: CallbackQuery, app):

        if callback.data is None:
            logger.error("[ROUTER] callback.data is None")
            await callback.answer()
            return

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

        # SAFE MESSAGE ACCESS (AIogram STRICT TYPE HANDLING)
        message = callback.message

        if message is None:
            logger.error("[ROUTER] callback.message is None")
            await callback.answer()
            return

        if isinstance(message, InaccessibleMessage):
            logger.error("[ROUTER] message is InaccessibleMessage (cannot edit)")
            await callback.answer()
            return

        # At this point: guaranteed Message
        await message.edit_text(
            view["text"],
            reply_markup=view["keyboard"]
        )

        await callback.answer()

        logger.info(f"[ROUTER] done {screen_id}")