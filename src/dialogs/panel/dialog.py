# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v7.7
# (hybrid UI formatting + unified renderer + preview/send parity)
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


def resolve_sender(dm: DialogManager) -> str:
    user = get_event_user(dm)

    if not user:
        return "unknown"

    if user.username:
        return f"@{user.username}"

    return user.full_name or "unknown"


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
# UI RENDERER (HYBRID CARD MODE)
# =========================

def build_block(data: dict, sender: str) -> str:
    """
    Hybrid Telegram UI layout:
    - structured header
    - section labels
    - boxed message via <pre>
    - consistent preview/send output
    """

    title = data.get("title") or "Untitled announcement"
    content = data.get("content") or ""

    return (
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📣 <b>ANNOUNCEMENT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        f"<pre><b>Title:</b> {title}\n\n
        
        f{content}</pre>\n\n"

        "────────────────────\n"
        f"👤 <b>Sent by:</b> {sender}\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


# =========================
# GETTERS
# =========================

async def preview_getter(dialog_manager: DialogManager, **_):
    data = dialog_manager.dialog_data or {}
    sender = resolve_sender(dialog_manager)

    return {
        "render": build_block(data, sender)
    }


# =========================
# NAVIGATION
# =========================

async def start_announcement(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    trace(dm, "START")
    await dm.switch_to(PanelSG.announcement_title)


async def back_to_main(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.main)


async def edit_title(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_title)


async def edit_content(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_content)


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

    if not bot:
        await callback.answer("Bot missing in middleware", show_alert=True)
        logger.error("[ANNOUNCEMENT] bot missing in middleware_data")
        return

    if not config:
        await callback.answer("Config missing in middleware", show_alert=True)
        logger.error("[ANNOUNCEMENT] config missing in middleware_data")
        return

    sender = resolve_sender(dm)
    message_text = build_block(data, sender)

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(chat_id, message_text, parse_mode="HTML")
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
        Button(Const("📣 Create announcement"), id="start", on_click=start_announcement)
    ),
    state=PanelSG.main,
)


title_window = Window(
    Const("📣 <b>Announcement Creator</b>\n\n📝 Enter title"),
    MessageInput(on_title_success),
    Row(
        Button(Const("⬅ Back"), id="back_main", on_click=back_to_main),
    ),
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("📣 <b>Announcement Creator</b>\n\n✍️ Write message"),
    MessageInput(on_content_success),
    Row(
        Button(Const("✏ Edit title"), id="edit_title", on_click=edit_title),
    ),
    state=PanelSG.announcement_content,
)


preview_window = Window(
    Format("{render}"),
    Row(
        Button(Const("✏ Edit title"), id="edit_title", on_click=edit_title),
        Button(Const("✏ Edit content"), id="edit_content", on_click=edit_content),
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