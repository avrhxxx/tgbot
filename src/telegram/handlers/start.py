from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager
from aiogram.fsm.context import FSMContext

from src.telegram.dialogs.home.state import HomeSG

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await message.answer(
        "👋 Welcome to Shadow Bot\n\n"
        "Loading your dashboard..."
    )

    # przejście do dialogu
    await dialog_manager.start(HomeSG.main)