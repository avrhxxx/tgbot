# =========================================
# FILE: src/dialogs/group_message/dialog.py
# =========================================

import logging

from aiogram import Bot
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
# TITLE STEP
# =========================

async def on_title(message: Message, widget, dm: DialogManager):
    title = (message.text or "").strip()

    if not title:
        title = "Announcement"

    dm.dialog_data["title"] = title
    logger.info("[GROUP MESSAGE] title set")

    await dm.switch_to(GroupMessageSG.content)


async def on_skip(callback: CallbackQuery, button, dm: DialogManager):
    dm.dialog_data["title"] = "Announcement"
    logger.info("[GROUP MESSAGE] title skipped")

    await dm.switch_to(GroupMessageSG.content)


# =========================
# CONTENT STEP
# =========================

async def on_content(message: Message, widget, dm: DialogManager):
    content = (message.text or "").strip()

    if not content:
        return

    dm.dialog_data["content"] = content
    logger.info("[GROUP MESSAGE] content set")

    await dm.switch_to(GroupMessageSG.preview)


# =========================
# SEND
# =========================

async def on_send(callback: CallbackQuery, button, dm: DialogManager):
    bot: Bot | None = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot:
        await callback.answer("Bot not available", show_alert=True)
        return

    if not config:
        await callback.answer("Config missing", show_alert=True)
        logger.error("[GROUP MESSAGE] config missing in middleware")
        return

    chat_ids = config.access.chat_ids

    title = dm.dialog_data.get("title", "Announcement")
    content = dm.dialog_data.get("content", "")

    event = dm.event
    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    text = render(title, content, sender)

    for chat_id in chat_ids:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"[GROUP MESSAGE] send failed chat_id={chat_id}: {e}")

    await callback.answer("Sent ✔")

    await dm.start(
        MainMenuSG.main,
        mode=StartMode.RESET_STACK,
    )


# =========================
# GETTER
# =========================

async def preview_getter(dm: DialogManager, **kwargs):
    event = dm.event
    user = getattr(event, "from_user", None)
    sender = user.full_name if user else "unknown"

    return {
        "preview": render(
            dm.dialog_data.get("title", "Announcement"),
            dm.dialog_data.get("content", ""),
            sender,
        )
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
    Const("Write your message:"),
    MessageInput(on_content),
    Row(
        Button(Const("Back"), id="back", on_click=lambda c, b, m: m.back()),
    ),
    state=GroupMessageSG.content,
)

preview_window = Window(
    Format("{preview}"),
    Row(
        Button(Const("Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(Const("Back"), id="back", on_click=lambda c, b, m: m.back()),
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