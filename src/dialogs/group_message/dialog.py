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
# RENDER
# =========================

def render(title: str, content: str, sender: str) -> str:
    return (
        "Group Message\n"
        "━━━━━━━━━━━━━━\n"
        f"<b>{title}</b>\n\n"
        "------\n"
        f"{content}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"<i>Author: {sender}</i>"
    )


# =========================
# TITLE
# =========================

async def on_title(message: Message, widget, dm: DialogManager):
    title = (message.text or "").strip()

    if not title:
        return

    dm.dialog_data["title"] = title
    logger.info("[GROUP MESSAGE] title set")

    await dm.switch_to(GroupMessageSG.content)


async def on_skip(callback: CallbackQuery, button, dm: DialogManager):
    dm.dialog_data["title"] = "Announcement"
    logger.info("[GROUP MESSAGE] title skipped")

    await dm.switch_to(GroupMessageSG.content)


# =========================
# CONTENT
# =========================

async def on_content(message: Message, widget, dm: DialogManager):
    content = (message.text or "").strip()

    if not content:
        return

    dm.dialog_data["content"] = content
    logger.info("[GROUP MESSAGE] content set")

    await dm.switch_to(GroupMessageSG.preview)


# =========================
# EDIT FROM PREVIEW
# =========================

async def edit_title(callback: CallbackQuery, button, dm: DialogManager):
    await dm.switch_to(GroupMessageSG.title)


async def edit_content(callback: CallbackQuery, button, dm: DialogManager):
    await dm.switch_to(GroupMessageSG.content)


# =========================
# SEND
# =========================

async def on_send(callback: CallbackQuery, button, dm: DialogManager):
    config = dm.middleware_data.get("config")
    bot = dm.middleware_data.get("bot")

    if not config or not bot:
        await callback.answer("Config/Bot missing", show_alert=True)
        return

    title = dm.dialog_data.get("title", "Announcement")
    content = dm.dialog_data.get("content", "")

    user = callback.from_user
    sender = user.full_name if user else "unknown"

    text = render(title, content, sender)

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(chat_id, text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"[GROUP MESSAGE] send failed -> {chat_id}: {e}")

    await callback.answer("Sent ✔")

    await dm.start(MainMenuSG.main, mode=StartMode.RESET_STACK)


# =========================
# GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    title = dialog_manager.dialog_data.get("title", "Announcement")
    content = dialog_manager.dialog_data.get("content", "")

    event = dialog_manager.event
    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    return {
        "preview": render(title, content, sender)
    }


# =========================
# WINDOWS
# =========================

title_window = Window(
    Const("Enter title (or skip):"),
    MessageInput(on_title),
    Row(
        Button(Const("Skip"), id="skip", on_click=on_skip),
    ),
    state=GroupMessageSG.title,
)

content_window = Window(
    Const("Enter message content:"),
    MessageInput(on_content),
    Row(
        Button(Const("Back"), id="back", on_click=lambda c, b, m: m.back()),
    ),
    state=GroupMessageSG.content,
)

preview_window = Window(
    Format("{preview}"),
    Row(
        Button(Const("Edit title"), id="edit_title", on_click=edit_title),
        Button(Const("Edit text"), id="edit_text", on_click=edit_content),
    ),
    Row(
        Button(Const("Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(Const("Back"), id="back", on_click=lambda c, b, m: m.back()),
    ),
    getter=preview_getter,
    state=GroupMessageSG.preview,
)


group_message_dialog = Dialog(
    title_window,
    content_window,
    preview_window,
)