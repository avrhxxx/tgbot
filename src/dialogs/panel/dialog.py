# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v6.6 (aiogram-dialog stable + fixed getter + production logging)
# =========================================

import logging
from typing import Optional, Tuple, Any

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
# DEBUG TRACE (SAFE)
# =========================

def trace(dm: DialogManager, label: str):
    try:
        ctx = dm.current_context()
        state = ctx.state
        state_repr = getattr(state, "state", str(state))
    except Exception as e:
        state_repr = f"UNKNOWN:{type(e).__name__}"

    logger.info(
        f"[ANNOUNCEMENT TRACE] {label} | state={state_repr} | data={dm.dialog_data}"
    )


# =========================
# NAVIGATION
# =========================

async def to_announcement_menu(callback, button, dm: DialogManager):
    trace(dm, "ENTER MENU")
    await dm.switch_to(PanelSG.announcement_menu)


async def back_to_main(callback, button, dm: DialogManager):
    trace(dm, "BACK MAIN")
    await dm.switch_to(PanelSG.main)


async def next_to_content(callback, button, dm: DialogManager):
    trace(dm, "NEXT -> CONTENT")
    await dm.switch_to(PanelSG.announcement_content)


async def back_to_title(callback, button, dm: DialogManager):
    trace(dm, "BACK -> TITLE")
    await dm.switch_to(PanelSG.announcement_title)


# =========================
# FLOW INPUT
# =========================

async def select_tag(callback, button, dm: DialogManager):
    dm.dialog_data["tag"] = button.widget_id
    trace(dm, f"TAG SELECTED {button.widget_id}")
    await dm.switch_to(PanelSG.announcement_title)


# ---------- TITLE ----------
async def on_title_success(message: types.Message, widget, dm: DialogManager):
    dm.dialog_data["title"] = (message.text or "").strip()
    logger.info(f"[ANNOUNCEMENT] title saved")
    await dm.next()


# ---------- CONTENT ----------
async def on_content_success(message: types.Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        await message.answer("❌ Content is required.")
        return

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    logger.info(f"[ANNOUNCEMENT] content saved")

    await message.answer("✔ Content saved. Opening preview...")
    trace(dm, "AUTO -> PREVIEW")

    await dm.next()


# =========================
# SEND ANNOUNCEMENT
# =========================

async def send_announcement(callback, button, dm: DialogManager):
    data = d(dm)

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        await callback.message.answer("❌ Missing bot/config")
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

    logger.info(f"[ANNOUNCEMENT] DONE sent={sent}")

    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>"),
    Row(Button(Const("📣 Create announcement"), id="announcement", on_click=to_announcement_menu)),
    state=PanelSG.main,
)


announcement_menu_window = Window(
    Const("📣 Select tag:"),
    Row(
        Button(Const("Tag1"), id="tag1", on_click=select_tag),
        Button(Const("Tag2"), id="tag2", on_click=select_tag),
    ),
    state=PanelSG.announcement_menu,
)


title_window = Window(
    Const("📣 Title (optional)"),
    MessageInput(on_title_success),
    Row(Button(Const("➡ Next"), id="next_title", on_click=next_to_content)),
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("✍️ Message (required)"),
    MessageInput(on_content_success),
    Row(Button(Const("⬅ Back"), id="back_content", on_click=back_to_title)),
    state=PanelSG.announcement_content,
)


# 🔥 FIXED PREVIEW (THIS WAS YOUR CRASH)
preview_window = Window(
    Format(
        "📣 <b>{title}</b>\n\n"
        "{content}\n\n"
        "────────────\n"
        "🏷 Tag: {tag}\n"
        "👤 Sent by: {sender}"
    ),
    Row(
        Button(Const("⬅ Back"), id="back_preview", on_click=back_to_title),
        Button(Const("🚀 Send"), id="send", on_click=send_announcement),
    ),
    getter=lambda **_: {},  # <- IMPORTANT: no dm argument
    state=PanelSG.announcement_preview,
)


panel_dialog = Dialog(
    main_window,
    announcement_menu_window,
    title_window,
    content_window,
    preview_window,
)