# src/handlers/common/start.py

from aiogram import types

from ui.screen_contracts import ScreenContext
from ui.screens.home.r3_home_screen import render as r3_home_screen


async def start_handler(message: types.Message, app):

    user_id = str(message.from_user.id)

    context: ScreenContext = {
        "app": app,
        "user_id": user_id,
        "callback": None
    }

    # -------------------------
    # TEMP: ONLY R3 HOME SCREEN
    # -------------------------
    result = await r3_home_screen(context)

    await message.answer(
        text=result["text"],
        reply_markup=result["keyboard"]
    )