# =========================================
# FILE: src/dialogs/group_message/dialog.py
# =========================================

import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.group_message.states import GroupMessageSG
from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


# =========================
# INPUT HANDLER
# =========================

async def on_message_input(message: Message, widget, dialog_manager: DialogManager):
    text = (message.text or "").strip()

    if not text:
        return

    dialog_manager.dialog_data["text"] = text
    logger.info(f"[GROUP MESSAGE] text saved")

    await dialog_manager.switch_to(GroupMessageSG.preview)


# =========================
# SEND HANDLER (placeholder)
# =========================

async def on_send(callback: CallbackQuery, button, dialog_manager: DialogManager):
    text = dialog_manager.dialog_data.get("text", "")

    logger.info(f"[GROUP MESSAGE] SEND -> {text}")

    await callback.answer("Sent (mock) ✔")

    # wracamy do main menu
    await dialog_manager.start(
        MainMenuSG.main,
        mode=dialog_manager.start_mode.RESET_STACK,
    )


# =========================
# GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "text": dialog_manager.dialog_data.get("text", "")
    }


# =========================
# WINDOWS
# =========================

input_window = Window(
    Const("📢 Send group message\n\nWrite your message:"),
    MessageInput(on_message_input),
    state=GroupMessageSG.input,
)

preview_window = Window(
    Format(
        "📢 Preview\n\n"
        "{text}"
    ),
    Row(
        Button(Const("🚀 Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(
            Const("🔙 Back"),
            id="back",
            on_click=lambda c, b, m: m.back(),
        )
    ),
    getter=preview_getter,
    state=GroupMessageSG.preview,
)


group_message_dialog = Dialog(
    input_window,
    preview_window,
)