from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.panel.states import PanelSG
from src.utils.access import can_use_panel

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    user = message.from_user
    if user is None:
        return

    if not can_use_panel(user.id):
        return

    # 🔥 KLUCZ: zawsze reset context
    await dialog_manager.start(
        PanelSG.main,
        mode=StartMode.RESET_STACK
    )