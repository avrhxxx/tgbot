# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard (stable dialog version)
# =========================================

import logging
from typing import Optional, Tuple

from aiogram import types
from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG

logger = logging.getLogger(__name__)


# =========================
# HELPERS
# =========================

def get_event_user(dm: DialogManager) -> User | None:
    event = dm.event

    if isinstance(event, Message):
        return event.from_user
    if isinstance(event, CallbackQuery):
        return event.from_user

    return None


def resolve_sender(dm: DialogManager) -> User | None:
    return get_event_user(dm)


def save_media(message: types.Message) -> Optional[Tuple[str, str]]:
    if message.photo:
        return ("photo", message.photo[-1].file_id)
    if message.video:
        return ("video", message.video.file_id)
    if message.document:
        return ("document", message.document.file_id)
    if message.animation:
        return ("animation", message.animation.file_id)
    return None


def trace(dm: DialogManager, label: str):
    try:
        state = dm.current_context().state
        state_repr = getattr(state, "state", str(state))
    except Exception:
        state_repr = "UNKNOWN"

    logger.info(f"[ANNOUNCEMENT] {label} | state={state_repr} | data={dm.dialog_data}")


# =========================
# UI RENDERER
# =========================

def build_block(data: dict, user: User | None) -> str:
    title_raw = data.get("title") or "UNTITLED ANNOUNCEMENT"
    title = title_raw.upper()

    content = data.get("content") or ""

    sender = (
        f'<a href="tg://user?id={user.id}">{user.full_name or "user"}</a>'
        if user else "UNKNOWN"
    )

    return (
        f"ANNOUNCEMENT: {title}\n"
        "━━━━━━━━━━━━━━\n"
        f"{sender}: {content}\n"
        "━━━━━━━━━━━━━━"
    )


# =========================
# GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **_):
    data = dialog_manager.dialog_data or {}
    user = resolve_sender(dialog_manager)

    return {"render": build_block(data, user)}


# =========================
# FLOW INPUT
# =========================

async def on_title_success(message: Message, widget, dm: DialogManager):
    dm.dialog_data["title"] = (message.text or "").strip()
    trace(dm, "TITLE SAVED")
    await dm.switch_to(PanelSG.announcement_content)


async def on_content_success(message: Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        return await dm.show()

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    trace(dm, "CONTENT SAVED")
    await dm.switch_to(PanelSG.announcement_preview)


# =========================
# SEND
# =========================

async def send_announcement(callback: CallbackQuery, button, dm: DialogManager):
    data = dm.dialog_data or {}

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        return

    user = resolve_sender(dm)
    message_text = build_block(data, user)

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(
                chat_id,
                message_text,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"[ANNOUNCEMENT] failed chat_id={chat_id}: {e}")

    await callback.answer("Sent ✔")
    trace(dm, "SENT")

    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 Moderator Panel"),
    Row(
        Button(Const("📣 Create announcement"), id="start", on_click=lambda c, b, m: m.switch_to(PanelSG.announcement_title)),
    ),
    state=PanelSG.main,
)


title_window = Window(
    Const("📝 Enter title"),
    MessageInput(on_title_success),
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("✍️ Write message"),
    MessageInput(on_content_success),
    state=PanelSG.announcement_content,
)


preview_window = Window(
    Format("{render}"),
    Row(
        Button(Const("✏ Edit title"), id="edit_title", on_click=lambda c, b, m: m.switch_to(PanelSG.announcement_title)),
        Button(Const("✏ Edit content"), id="edit_content", on_click=lambda c, b, m: m.switch_to(PanelSG.announcement_content)),
    ),
    Row(
        Button(Const("🚀 Send"), id="send", on_click=send_announcement),
    ),
    getter=preview_getter,
    state=PanelSG.announcement_preview,
)


panel_dialog = Dialog(
    main_window,
    title_window,
    content_window,
    preview_window,
)