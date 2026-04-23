# src/handlers/common/start.py

from aiogram import types
from ui.screen_engine import ScreenEngine
from ui.screen_contracts import ScreenContext


async def start_handler(message: types.Message, app):
    user_id = str(message.from_user.id)

    context = {
        "app": app,
        "user_id": user_id
    }

    screen = await ScreenEngine.resolve_home_screen(context)

    result = await screen(context)

    await message.answer(
        text=result["text"],
        reply_markup=result["keyboard"]
    )