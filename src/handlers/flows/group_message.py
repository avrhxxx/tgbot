# =========================================
# FILE: src/handlers/flows/group_message.py
# =========================================

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "menu:group_message")
async def open_group_message(callback: CallbackQuery):
    if not callback.message:
        return

    logger.info("📢 UI FLOW: group_message opened")

    await callback.message.edit_text(
        "📢 GROUP MESSAGE\n\n"
        "This is UI placeholder flow.\n\n"
        "Choose action:",
        reply_markup=None  # na razie brak keyboarda
    )

    await callback.answer()


@router.callback_query(F.data == "menu:back")
async def back(callback: CallbackQuery):
    if not callback.message:
        return

    from src.ui.main_menu import format_main_menu
    from src.ui.keyboards.main_menu import main_menu_kb

    user = callback.from_user

    await callback.message.edit_text(
        format_main_menu(user),
        reply_markup=main_menu_kb()
    )

    await callback.answer()