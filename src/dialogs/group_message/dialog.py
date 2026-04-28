# =========================================
# FILE: src/dialogs/group_message/dialog.py
# =========================================

import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.group_message.states import GroupMessageSG
from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


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
# STEP 1 — TITLE
# =========================

async def on_title_input(message: Message, widget, dialog_manager: DialogManager):
    title = (message.text or "").strip()

    if not title:
        return

    dialog_manager.dialog_data["title"] = title
    logger.info("[GROUP MESSAGE] title set")

    await dialog_manager.switch_to(GroupMessageSG.content)


async def on_skip_title(callback: CallbackQuery, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["title"] = "Announcement"
    logger.info("[GROUP MESSAGE] title skipped")

    await dialog_manager.switch_to(GroupMessageSG.content)


# =========================
# STEP 2 — CONTENT
# =========================

async def on_content_input(message: Message, widget, dialog_manager: DialogManager):
    text = (message.text or "").strip()

    if not text:
        return

    dialog_manager.dialog_data["text"] = text
    logger.info("[GROUP MESSAGE] content set")

    await dialog_manager.switch_to(GroupMessageSG.preview)


# =========================
# SEND HANDLER
# =========================

async def on_send(callback: CallbackQuery, button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data

    title = data.get("title", "Announcement")
    text = data.get("text", "")

    config = dialog_manager.middleware_data.get("config")
    bot = dialog_manager.middleware_data.get("bot")

    user = callback.from_user
    sender = user.full_name if user else "unknown"

    message_text = render_group_message(title, text, sender)

    if not config or not bot:
        await callback.answer("Config or bot missing", show_alert=True)
        logger.error("[GROUP MESSAGE] missing config/bot")
        return

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(chat_id, message_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"[GROUP MESSAGE] send failed -> {chat_id}: {e}")

    logger.info("[GROUP MESSAGE] sent to all chats")

    await callback.answer("Sent ✔")

    await dialog_manager.start(
        MainMenuSG.main,
        mode=StartMode.RESET_STACK,
    )


# =========================
# GETTER (FIXED!)
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data

    title = data.get("title", "Announcement")
    text = data.get("text", "")

    event = dialog_manager.event
    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    return {
        "preview": render_group_message(title, text, sender)
    }


# =========================
# WINDOWS
# =========================

title_window = Window(
    Const(
        "Group Message\n\n"
        "Enter title (or skip):"
    ),
    MessageInput(on_title_input),
    Row(
        Button(Const("Skip"), id="skip_title", on_click=on_skip_title),
    ),
    state=GroupMessageSG.title,
)

content_window = Window(
    Const(
        "Group Message\n\n"
        "Enter message content:"
    ),
    MessageInput(on_content_input),
    state=GroupMessageSG.content,
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
            on_click=lambda c, b, m: m.switch_to(GroupMessageSG.content),
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
    content_window,
    preview_window,
)