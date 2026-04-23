# src/handlers/r3/home_router.py

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data.startswith("nav."))
async def handle_navigation(callback: CallbackQuery, **data):
    app = data.get("app")

    screen_router = app.engines.get("screen_router")

    await screen_router.handle(callback, app)