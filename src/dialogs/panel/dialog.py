# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v6.7 (conversational UX + aiogram-dialog stable + fixed preview + production logging)
# =========================================

import logging
from typing import Optional, Tuple

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG

logger = logging.getLogger(__name__)


# =========================
# HELPERS
# =========================

def d(dm: DialogManager) -> dict:
    return dm.dialog_data or {}


def extract_user(dm: DialogManager):
    event = dm.event
    if isinstance(event, Message):
        return event.from_user
    if isinstance(event, CallbackQuery):
        return event.from_user
    return None


def resolve_sender(dm: DialogManager) -> str:
    user = extract_user(dm)

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


# =========================
# DEBUG TRACE
# =========================

def trace(dm: DialogManager, label: str):
    try:
        ctx = dm.current_context()
        state = ctx.state
        state_repr = getattr(state, "state", str(state))
    except Exception as e:
        state_repr = f"UNKNOWN:{type(e).__name__}"

    logger.info(f"[ANNOUNCEMENT] {label} | state={state_repr} | data={dm.dialog_data}")


# =========================
# NAVIGATION (CONVERSATIONAL)
# =========================

async def to_announcement_menu(callback, button, dm: DialogManager):
    trace(dm, "START FLOW")
    await callback.message.answer("📣 Alright, let’s create a new announcement.")
    await dm.switch_to(PanelSG.announcement_menu)


async def back_to_main(callback, button, dm: DialogManager):
    trace(dm, "EXIT FLOW")
    await callback.message.answer("↩️ Back to main panel.")
    await dm.switch_to(PanelSG.main)


async def next_to_content(callback, button, dm: DialogManager):
    trace(dm, "ASK CONTENT")
    await callback.message.answer("✍️ Now tell me what you want to send.")
    await dm.switch_to(PanelSG.announcement_content)


async def back_to_title(callback, button, dm: DialogManager):
    trace(dm, "BACK TO TITLE")
    await callback.message.answer("📝 Let’s adjust the title.")
    await dm.switch_to(PanelSG.announcement_title)


# =========================
# FLOW INPUT
# =========================

async def select_tag(callback, button, dm: DialogManager):
    dm.dialog_data["tag"] = button.widget_id
    trace(dm, f"TAG SET: {button.widget_id}")

    await callback.message.answer("✔ Got it. Now give your announcement a title (or skip it).")
    await dm.switch_to(PanelSG.announcement_title)


# ---------- TITLE ----------
async def on_title_success(message: types.Message, widget, dm: DialogManager):
    dm.dialog_data["title"] = (message.text or "").strip()

    logger.info("[ANNOUNCEMENT] title saved")

    await message.answer("✔ Title saved. Next step — write the message.")
    await dm.next()


# ---------- CONTENT ----------
async def on_content_success(message: types.Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        await message.answer("❌ Please write something for the announcement.")
        return

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    logger.info("[ANNOUNCEMENT] content saved")

    await message.answer("✔ Perfect. Let me show you a preview...")
    trace(dm, "GO PREVIEW")

    await dm.next()


# =========================
# SEND ANNOUNCEMENT
# =========================

async def send_announcement(callback, button, dm: DialogManager):
    data = d(dm)

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        await callback.message.answer("❌ Bot configuration missing.")
        return

    title = data.get("title") or "Announcement"
    content = data.get("content") or ""
    tag = data.get("tag") or "unknown"
    media = data.get("media")

    sender = resolve_sender(dm)

    caption = (
        f"📣 <b>{title}</b>\n\n"
        f"{content}\n\n"
        f"────────────\n"
        f"🏷 Tag: {tag}\n"
        f"👤 Sent by: {sender}"
    )

    sent = 0

    for chat_id in config.access.chat_ids:
        try:
            if media:
                mtype, file_id = media

                if mtype == "photo":
                    await bot.send_photo(chat_id, file_id, caption=caption)
                elif mtype == "video":
                    await bot.send_video(chat_id, file_id, caption=caption)
                elif mtype == "document":
                    await bot.send_document(chat_id, file_id, caption=caption)
                elif mtype == "animation":
                    await bot.send_animation(chat_id, file_id, caption=caption)
            else:
                await bot.send_message(chat_id, caption)

            sent += 1

        except Exception as e:
            logger.warning(f"[ANNOUNCEMENT] failed chat_id={chat_id}: {e}")

    logger.info(f"[ANNOUNCEMENT] SENT SUCCESSFULLY -> {sent} chats")

    await callback.message.answer("🚀 Announcement sent successfully!")
    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS (CONVERSATIONAL UX)
# =========================

main_window = Window(
    Const("🛠 Welcome back, Moderator."),
    Row(
        Button(Const("📣 Create announcement"), id="announcement", on_click=to_announcement_menu)
    ),
    state=PanelSG.main,
)


announcement_menu_window = Window(
    Const("📣 What kind of announcement is this?"),
    Row(
        Button(Const("Tag1"), id="tag1", on_click=select_tag),
        Button(Const("Tag2"), id="tag2", on_click=select_tag),
    ),
    state=PanelSG.announcement_menu,
)


title_window = Window(
    Const("📝 Give your announcement a title (optional)"),
    MessageInput(on_title_success),
    Row(Button(Const("➡ Continue"), id="next_title", on_click=next_to_content)),
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("✍️ Write your announcement message"),
    MessageInput(on_content_success),
    Row(Button(Const("⬅ Back"), id="back_content", on_click=back_to_title)),
    state=PanelSG.announcement_content,
)


preview_window = Window(
    Format(
        "📣 <b>{title}</b>\n\n"
        "{content}\n\n"
        "────────────\n"
        "🏷 Tag: {tag}\n"
        "👤 Sent by: {sender}"
    ),
    Row(
        Button(Const("⬅ Edit"), id="back_preview", on_click=back_to_title),
        Button(Const("🚀 Send now"), id="send", on_click=send_announcement),
    ),
    getter=lambda dm, **_: {
        "title": d(dm).get("title") or "Announcement",
        "content": d(dm).get("content") or "",
        "tag": d(dm).get("tag") or "unknown",
        "sender": resolve_sender(dm),
    },
    state=PanelSG.announcement_preview,
)


panel_dialog = Dialog(
    main_window,
    announcement_menu_window,
    title_window,
    content_window,
    preview_window,
)