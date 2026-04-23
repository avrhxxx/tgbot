# src/ui/screen_router.py

from aiogram.types import CallbackQuery


class ScreenRouter:
    """
    Translates callback_data → screen_id
    """

    def __init__(self, registry):
        self.registry = registry

    def resolve(self, callback_data: str) -> str:
        """
        nav.events → events
        screen:events → events
        """

        if callback_data.startswith("nav."):
            return callback_data.replace("nav.", "")

        if callback_data.startswith("screen:"):
            return callback_data.split(":")[1]

        return callback_data

    async def handle(self, callback: CallbackQuery, app):
        screen_id = self.resolve(callback.data)

        user_id = str(callback.from_user.id)

        view = self.registry.render(
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