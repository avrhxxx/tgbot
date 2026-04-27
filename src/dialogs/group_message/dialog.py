# =========================================
# FILE: src/dialogs/group_message/dialog.py
# =========================================

import logging

from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.group_message.states import GroupMessageSG
from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


# =========================
# ANNOUNCEMENT RENDERER (OLD STYLE)
# =========================

def render_group_message(title: str, text: str, sender: str) -> str:
    return (
        "Group Message\n"
        "━━━━━━━━━━━━━━\n"
        f"<b>{title}</b>\n\n"
        "------\n"
        f"{text}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"<i>Author: {sender}</i>"
    )


# =========================
# INPUT HANDLER
# =========================

async def on_message_input(message: Message, widget, dialog_manager: DialogManager):
    text = (message.text or "").strip()

    if not text:
        return

    dialog_manager.dialog_data["text"] = text
    logger.info("[GROUP MESSAGE] text saved")

    await dialog_manager.switch_to(GroupMessageSG.preview)


# =========================
# SEND HANDLER
# =========================

async def on_send(callback: CallbackQuery, button, dialog_manager: DialogManager):
    text = dialog_manager.dialog_data.get("text", "")

    logger.info(f"[GROUP MESSAGE] SEND -> {text}")

    await callback.answer("Sent (mock) ✔")

    await dialog_manager.start(
        MainMenuSG.main,
        mode=StartMode.RESET_STACK,
    )


# =========================
# GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    user: User | None = dialog_manager.event.from_user if dialog_manager.event else None

    text = dialog_manager.dialog_data.get("text", "")
    title = "Announcement"
    sender = user.full_name if user else "unknown"

    return {
        "preview": render_group_message(title, text, sender)
    }


# =========================
# WINDOWS
# =========================

input_window = Window(
    Const(
        "Group Message\n\n"
        "Write your message:"
    ),
    MessageInput(on_message_input),
    state=GroupMessageSG.input,
)

preview_window = Window(
    Format("{preview}"),
    Row(
        Button(Const("🚀 Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(
            Const("🔙 Back"),
            id="back",
            on_click=lambda c, b, m: m.switch_to(GroupMessageSG.input),
        )
    ),
    getter=preview_getter,
    state=GroupMessageSG.preview,
)


group_message_dialog = Dialog(
    input_window,
    preview_window,
)