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

    # safety log (optional but useful for debugging flow)
    print(f"[START] user_id={message.from_user.id}")

    # 🚀 Start dialog flow (explicit reset = safest in production)
    await dialog_manager.start(
        state=HomeSG.main,
        mode="RESET_STACK"
    )