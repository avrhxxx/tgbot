# src/telegram/handlers/start.py
# =========================================
# GROUP: telegram.handlers
# FILE: start.py
# DESCRIPTION:
# Entry handler for /start command.
# Responsible for routing user into Home flow.
# =========================================

from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(commands=["start"])
async def start_handler(message: Message):
    """
    Entry point of the bot.
    Later this will route to aiogram-dialog Home window.
    """

    await message.answer(
        "👋 Welcome to Shadow Bot\n\n"
        "Loading your dashboard..."
    )

    # TODO:
    # - load user (telegram_id)
    # - resolve role (R3/R4/R5)
    # - route to dialog HOME window