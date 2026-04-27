# =========================================
# FILE: src/handlers/flows/group_message.py
# DESCRIPTION:
# Announcement / Group Message flow (placeholder UI)
# =========================================

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.ui.keyboards.group_message import group_message_kb
from src.ui.main_menu import format_main_menu
from src.ui.keyboards.main_menu import main_menu_kb

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "flow:group_message")
async def open_group_message(callback: CallbackQuery):
    logger.info(f"GROUP_MESSAGE | open | user={callback.from_user.id}")

    text = (
        "GROUP MESSAGE\n\n"
        "This is a placeholder flow.\n"
        "Next: n8n integration or dialog wizard."
    )

    await callback.message.edit_text(
        text,
        reply_markup=group_message_kb()
    )

    await callback.answer()


@router.callback_query(F.data == "nav:back")
async def back_to_menu(callback: CallbackQuery):
    logger.info(f"BACK | user={callback.from_user.id}")

    await callback.message.edit_text(
        format_main_menu(callback.from_user),
        reply_markup=main_menu_kb()
    )

    await callback.answer()