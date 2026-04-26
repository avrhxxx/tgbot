# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + broadcast wizard v2 (UX chat-style + media + preview)
# =========================================

import logging

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG

logger = logging.getLogger(__name__)


# =========================
# HELPERS
# =========================

def data(dm: DialogManager) -> dict:
    return dm.dialog_data or {}


# =========================
# NAVIGATION
# =========================

async def to_broadcast_menu(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.broadcast_menu)


async def back_to_main(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.main)


# =========================
# FLOW
# =========================

# --- TAG ---
async def select_tag(callback, button, dm: DialogManager):
    dm.dialog_data["tag"] = button.widget_id
    await dm.switch_to(PanelSG.broadcast_title)


# --- TITLE (UX MODE) ---
async def save_title(message: types.Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        await message.answer("❌ Please send a valid title")
        return

    dm.dialog_data["title"] = text
    logger.info("Title saved")

    await message.answer("✍️ Nice. Now send me the broadcast content.")
    await dm.switch_to(PanelSG.broadcast_content)


# --- CONTENT + MEDIA SUPPORT ---
async def save_content(message: types.Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        await message.answer("❌ Please send valid content")
        return

    media = None

    # support photo/video/document/gif
    if message.photo:
        media = ("photo", message.photo[-1].file_id)
    elif message.video:
        media = ("video", message.video.file_id)
    elif message.document:
        media = ("document", message.document.file_id)
    elif message.animation:
        media = ("animation", message.animation.file_id)

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = media

    logger.info("Content + media saved")

    await dm.switch_to(PanelSG.broadcast_preview)


# =========================
# SEND BROADCAST
# =========================

async def send_broadcast(callback, button, dm: DialogManager):
    d = data(dm)

    title = d.get("title", "No title")
    content = d.get("content", "No content")
    tag = d.get("tag", "unknown")
    media = d.get("media")

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
        f"👤 Sent by moderator"
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
            logger.warning(f"Send failed {chat_id}: {e}")

    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>\n\nChoose action:"),
    Row(
        Button(Const("📣 Broadcast"), id="broadcast", on_click=to_broadcast_menu),
    ),
    state=PanelSG.main,
)


broadcast_menu_window = Window(
    Const("📣 Choose a broadcast tag:"),
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


# --- UX TITLE STEP ---
title_window = Window(
    Const("📣 What should be the title of this broadcast?"),
    MessageInput(save_title),
    state=PanelSG.broadcast_title,
)


# --- UX CONTENT STEP ---
content_window = Window(
    Const("✍️ Now send the message content (you can also attach media)"),
    MessageInput(save_content),
    state=PanelSG.broadcast_content,
)


# --- PREVIEW (REALISTIC TELEGRAM STYLE) ---
preview_window = Window(
    Format(
        "📣 <b>{title}</b>\n\n"
        "{content}\n\n"
        "────────────\n"
        "🏷 Tag: {tag}\n"
        "👤 Sent by moderator"
    ),
    Row(
        Button(Const("🚀 Send broadcast"), id="send", on_click=send_broadcast),
    ),
    state=PanelSG.broadcast_preview,
)


panel_dialog = Dialog(
    main_window,
    broadcast_menu_window,
    title_window,
    content_window,
    preview_window,
)