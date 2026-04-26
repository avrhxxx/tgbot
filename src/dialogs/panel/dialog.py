# src/dialogs/panel/dialog.py
# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + broadcast wizard (MVP single-dialog flow)
# =========================================

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG


# =========================
# NAVIGATION
# =========================

async def to_broadcast_menu(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.broadcast_menu)


async def back_to_main(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.main)


# =========================
# BROADCAST FLOW
# =========================

# --- TAG SELECT ---
async def select_tag(callback, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["tag"] = button.widget_id
    await dialog_manager.switch_to(PanelSG.broadcast_title)


# --- TITLE INPUT ---
async def save_title(message: types.Message, widget, dialog_manager: DialogManager):
    dialog_manager.dialog_data["title"] = message.text
    await dialog_manager.switch_to(PanelSG.broadcast_content)


# --- CONTENT INPUT ---
async def save_content(message: types.Message, widget, dialog_manager: DialogManager):
    dialog_manager.dialog_data["content"] = message.text
    await dialog_manager.switch_to(PanelSG.broadcast_preview)


# --- SEND ---
async def send_broadcast(callback, button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data

    text = (
        f"📣 <b>{data.get('title')}</b>\n\n"
        f"{data.get('content')}\n\n"
        f"────────────\n"
        f"🏷 Tag: {data.get('tag')}\n"
        f"👤 Sent by system"
    )

    chat_ids = dialog_manager.middleware_data["config"].access.chat_ids
    bot = dialog_manager.middleware_data["bot"]

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text)
        except Exception:
            continue

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


# --- BROADCAST MENU (TAGS) ---
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


# --- TITLE ---
title_window = Window(
    Const("📝 Send broadcast title:"),
    MessageInput(save_title),
    state=PanelSG.broadcast_title,
)


# --- CONTENT ---
content_window = Window(
    Const("✍️ Send broadcast content:"),
    MessageInput(save_content),
    state=PanelSG.broadcast_content,
)


# --- PREVIEW ---
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