# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + broadcast wizard v6 (fixed UX flow + stable aiogram-dialog state handling)
# =========================================

import logging
from typing import Optional, Tuple

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row

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


async def safe_show(dm: DialogManager):
    """
    IMPORTANT FIX:
    forces dialog refresh after MessageInput updates
    """
    await dm.show()


# =========================
# NAVIGATION
# =========================

async def to_broadcast_menu(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.broadcast_menu)


async def back_to_main(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.main)


async def next_to_content(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.broadcast_content)


async def back_to_title(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.broadcast_title)


async def next_to_preview(callback, button, dm: DialogManager):
    content = d(dm).get("content")

    if not content:
        await callback.message.answer("❌ Please send content first (required).")
        return

    await dm.switch_to(PanelSG.broadcast_preview)


# =========================
# FLOW INPUT HANDLERS
# =========================

async def select_tag(callback, button, dm: DialogManager):
    dm.dialog_data["tag"] = button.widget_id
    await dm.switch_to(PanelSG.broadcast_title)


# ---------- TITLE (OPTIONAL) ----------
async def save_title(message: types.Message, widget, dm: DialogManager):
    dm.dialog_data["title"] = (message.text or "").strip()
    await message.answer("✔ Title saved (optional). Click NEXT to continue.")
    await safe_show(dm)


# ---------- CONTENT (REQUIRED) ----------
async def save_content(message: types.Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        await message.answer("❌ Content is required. Please send a message.")
        return

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    await message.answer("✔ Content saved. Click NEXT to preview.")
    await safe_show(dm)


# =========================
# SEND BROADCAST
# =========================

async def send_broadcast(callback, button, dm: DialogManager):
    data = d(dm)

    title = data.get("title") or "Broadcast"
    content = data.get("content") or ""
    tag = data.get("tag") or "unknown"
    media = data.get("media")

    sender = resolve_sender(dm)

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        await callback.message.answer("❌ Missing bot/config")
        return

    caption = (
        f"📣 <b>{title}</b>\n\n"
        f"{content}\n\n"
        f"────────────\n"
        f"🏷 Tag: {tag}\n"
        f"👤 Sent by: {sender}"
    )

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

        except Exception as e:
            logger.warning(f"Broadcast failed for {chat_id}: {e}")

    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>"),
    Row(
        Button(Const("📣 Create broadcast"), id="broadcast", on_click=to_broadcast_menu),
    ),
    state=PanelSG.main,
)


broadcast_menu_window = Window(
    Const("📣 Select tag:"),
    Row(
        Button(Const("Tag1"), id="tag1", on_click=select_tag),
        Button(Const("Tag2"), id="tag2", on_click=select_tag),
    ),
    Row(
        Button(Const("Tag3"), id="tag3", on_click=select_tag),
        Button(Const("Tag4"), id="tag4", on_click=select_tag),
    ),
    Row(
        Button(Const("⬅ Back"), id="back", on_click=back_to_main),
    ),
    state=PanelSG.broadcast_menu,
)


# =========================
# STEP 1 - TITLE (OPTIONAL)
# =========================

title_window = Window(
    Const(
        "📣 How should your broadcast be titled?\n"
        "(optional — you can skip this step)"
    ),
    Row(
        Button(Const("➡ Next"), id="next_title", on_click=next_to_content),
    ),
    state=PanelSG.broadcast_title,
)


# =========================
# STEP 2 - CONTENT (REQUIRED)
# =========================

content_window = Window(
    Const(
        "✍️ What would you like to say?\n"
        "(required — send a message below)"
    ),
    Row(
        Button(Const("⬅ Back"), id="back_content", on_click=back_to_title),
        Button(Const("➡ Next"), id="next_content", on_click=next_to_preview),
    ),
    state=PanelSG.broadcast_content,
)


# =========================
# PREVIEW (SAFE + NO CRASH)
# =========================

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
        Button(Const("🚀 Send"), id="send", on_click=send_broadcast),
    ),
    getter=lambda dm, **_: {
        "title": d(dm).get("title") or "Broadcast",
        "content": d(dm).get("content") or "",
        "tag": d(dm).get("tag") or "unknown",
        "sender": resolve_sender(dm),
    },
    state=PanelSG.broadcast_preview,
)


# =========================
# DIALOG
# =========================

panel_dialog = Dialog(
    main_window,
    broadcast_menu_window,
    title_window,
    content_window,
    preview_window,
)