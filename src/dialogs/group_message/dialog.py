# =========================================
# FILE: src/dialogs/group_message/dialog.py
# =========================================

import logging
import os

from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.group_message.states import GroupMessageSG
from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


# =========================
# ENV PARSER
# =========================

def parse_chat_ids() -> list[int]:
    raw = os.getenv("CHAT_IDS", "")
    return [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]


# =========================
# RENDERER
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
# TITLE HANDLERS
# =========================

async def on_title_input(message: Message, widget, dialog_manager: DialogManager):
    title = (message.text or "").strip()

    if not title:
        title = "Announcement"

    dialog_manager.dialog_data["title"] = title

    logger.info("[GROUP MESSAGE] title saved")

    await dialog_manager.switch_to(GroupMessageSG.input)


async def on_skip_title(callback: CallbackQuery, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["title"] = "Announcement"

    logger.info("[GROUP MESSAGE] title skipped")

    await dialog_manager.switch_to(GroupMessageSG.input)


# =========================
# CONTENT HANDLER
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
    bot: Bot | None = dialog_manager.middleware_data.get("bot")

    if not bot:
        await callback.answer("Bot not available", show_alert=True)
        return

    title = dialog_manager.dialog_data.get("title", "Announcement")
    text = dialog_manager.dialog_data.get("text", "")

    event = dialog_manager.event
    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    message = render_group_message(title, text, sender)

    chat_ids = parse_chat_ids()

    for chat_id in chat_ids:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"[GROUP MESSAGE] failed chat_id={chat_id}: {e}")

    await callback.answer("Sent ✔")

    await dialog_manager.start(
        MainMenuSG.main,
        mode=StartMode.RESET_STACK,
    )


# =========================
# GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    event = dialog_manager.event

    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    title = dialog_manager.dialog_data.get("title", "Announcement")
    text = dialog_manager.dialog_data.get("text", "")

    return {
        "preview": render_group_message(title, text, sender)
    }


# =========================
# WINDOWS
# =========================

title_window = Window(
    Const(
        "Step 1/2\nEnter title:"
    ),
    MessageInput(on_title_input),
    Row(
        Button(
            Const("Skip"),
            id="skip_title",
            on_click=on_skip_title,
        )
    ),
    state=GroupMessageSG.title,
)

input_window = Window(
    Const(
        "Step 2/2\nWrite your message:"
    ),
    MessageInput(on_message_input),
    state=GroupMessageSG.input,
)

preview_window = Window(
    Format("{preview}"),
    Row(
        Button(Const("Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(
            Const("Back"),
            id="back",
            on_click=lambda c, b, m: m.back(),
        )
    ),
    getter=preview_getter,
    state=GroupMessageSG.preview,
)


# =========================
# DIALOG
# =========================

group_message_dialog = Dialog(
    title_window,
    input_window,
    preview_window,
)