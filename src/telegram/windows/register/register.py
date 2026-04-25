# =========================================
# GROUP: telegram.windows.register
# FILE: register.py
# DESCRIPTION:
# User onboarding window (UI layer only).
# =========================================

import logging

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import TextInput

from src.telegram.states.register import RegisterSG
from src.services.user.onboarding_service import onboarding_service

logger = logging.getLogger(__name__)


async def on_nick_enter(message, widget, dialog_manager: DialogManager, value: str):
    user_id = message.from_user.id

    onboarding_service.register_user(user_id, value)

    logger.info("Onboarding completed | user=%s", user_id)

    await dialog_manager.done()


register_window = Window(
    Format(
        "🎮 Welcome!\n\n"
        "Please enter your in-game nickname:"
    ),
    TextInput(
        id="nick_input",
        on_success=on_nick_enter,
    ),
    state=RegisterSG.waiting_for_nick,
)