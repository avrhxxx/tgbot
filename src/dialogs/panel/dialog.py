# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + broadcast wizard (MVP single-dialog flow)
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
# NAVIGATION
# =========================

async def to_broadcast_menu(callback, button, dialog_manager: DialogManager):
    logger.info("Navigating to broadcast menu")
    await dialog_manager.switch_to(PanelSG.broadcast_menu)


async def back_to_main(callback, button, dialog_manager: DialogManager):
    logger.info("Back to main panel")
    await dialog_manager.switch_to(PanelSG.main)


# =========================
# BROADCAST FLOW
# =========================

# --- TAG SELECT ---
async def select_tag(callback, button, dialog_manager: DialogManager):
    tag = button.widget_id
    dialog_manager.dialog_data["tag"] = tag

    logger.info(f"Broadcast tag selected: {tag}")

    await dialog_manager.switch_to(PanelSG.broadcast_title)


# --- TITLE INPUT ---
async def save_title(message: types.Message, widget, dialog_manager: DialogManager):
    title = message.text or ""
    dialog_manager.dialog_data["title"] = title

    logger.info(f"Broadcast title set: {title}")

    await dialog_manager.switch_to(PanelSG.broadcast_content)


# --- CONTENT INPUT ---
async def save_content(message: types.Message, widget, dialog_manager: DialogManager):
    content = message.text or ""
    dialog_manager.dialog_data["content"] = content

    logger.info("Broadcast content received")

    await dialog_manager.switch_to(PanelSG.broadcast_preview)


# --- SEND BROADCAST ---
async def send_broadcast(callback, button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data

    title = data.get("title", "")
    content = data.get("content", "")
    tag = data.get("tag", "unknown")

    text = (
        f"📣 <b>{title}</b>\n\n"
        f"{content}\n\n"
        f"────────────\n"
        f"🏷 Tag: {tag}\n"
        f"👤 Sent by: system"
    )

    bot = dialog_manager.middleware_data.get("bot")
    config = dialog_manager.middleware_data.get("config")

    if not bot or not config:
        logger.error("Bot or config missing in middleware_data")
        await callback.message.answer("❌ Bot/config not available")
        return

    chat_ids = config.access.chat_ids

    sent = 0

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text)
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send to {chat_id}: {e}")

    logger.info(f"Broadcast sent to {sent}/{len(chat_ids)} chats")

    await dialog_manager.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>\n\nChoose an action:"),
    Row(
        Button(Const("📣 Broadcast"), id="broadcast", on_click=to_broadcast_menu),
    ),
    state=PanelSG.main,
)


broadcast_menu_window = Window(
    Const("📣 <b>Select Broadcast Tag</b>"),
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


title_window = Window(
    Const("📝 Send broadcast title:"),
    MessageInput(save_title),
    state=PanelSG.broadcast_title,
)


content_window = Window(
    Const("✍️ Send broadcast content:"),
    MessageInput(save_content),
    state=PanelSG.broadcast_content,
)


preview_window = Window(
    Format(
        "📣 <b>{title}</b>\n\n"
        "{content}\n\n"
        "────────────\n"
        "🏷 Tag: {tag}\n"
        "👤 Sent by: system"
    ),
    Row(
        Button(Const("🚀 Send"), id="send", on_click=send_broadcast),
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