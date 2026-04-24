from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.telegram.dialogs.home.state import HomeSG

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    """
    Entry point of the bot.
    Routes directly into Home dialog (R3 base UI).
    """

    # 🚀 Direct transition to UI (no intermediate message)
    await dialog_manager.start(HomeSG.main)