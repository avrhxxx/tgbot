# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v7.2
# (pure dialog UX + per-user tags + pagination + clean headers)
# =========================================

import logging
from typing import Optional, Tuple, Dict, List

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Select
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG

logger = logging.getLogger(__name__)


# =========================
# PER-USER TAG STORAGE
# =========================

USER_TAGS: Dict[int, List[str]] = {}

PAGE_SIZE = 6


# =========================
# HELPERS
# =========================

def d(dm: DialogManager) -> dict:
    return dm.dialog_data or {}


def get_user_id(dm: DialogManager) -> int:
    event = dm.event
    if isinstance(event, Message):
        return event.from_user.id
    if isinstance(event, CallbackQuery):
        return event.from_user.id
    return 0


def resolve_sender(dm: DialogManager) -> str:
    user = dm.event.from_user
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
# GETTERS
# =========================

async def tags_getter(dialog_manager: DialogManager, **_):
    user_id = get_user_id(dialog_manager)

    tags = USER_TAGS.get(user_id, [])
    page = dialog_manager.dialog_data.get("page", 0)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    return {
        "tags": tags[start:end],
        "has_prev": page > 0,
        "has_next": end < len(tags),
        "page": page,
    }


async def title_getter(dialog_manager: DialogManager, **_):
    return {
        "tag": d(dialog_manager).get("tag", "unknown"),
    }


async def preview_getter(dialog_manager: DialogManager, **_):
    data = d(dialog_manager)
    return {
        "title": data.get("title") or "Announcement",
        "content": data.get("content") or "",
        "tag": data.get("tag") or "unknown",
        "sender": resolve_sender(dialog_manager),
    }


# =========================
# NAVIGATION
# =========================

async def to_announcement_menu(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    dm.dialog_data["page"] = 0
    await dm.switch_to(PanelSG.announcement_menu)


async def to_create_tag(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer("Type tag name")
    await dm.switch_to(PanelSG.create_tag)


async def next_page(callback: CallbackQuery, button, dm: DialogManager):
    dm.dialog_data["page"] = dm.dialog_data.get("page", 0) + 1
    await callback.answer()
    await dm.show()


async def prev_page(callback: CallbackQuery, button, dm: DialogManager):
    dm.dialog_data["page"] = max(dm.dialog_data.get("page", 0) - 1, 0)
    await callback.answer()
    await dm.show()


async def next_to_content(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_content)


async def back_to_title(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_title)


# =========================
# TAG HANDLING
# =========================

async def select_tag(callback: CallbackQuery, widget, dm: DialogManager, item_id: str):
    dm.dialog_data["tag"] = item_id
    await callback.answer(f"{item_id} selected")
    await dm.switch_to(PanelSG.announcement_title)


async def create_tag_input(message: Message, widget, dm: DialogManager):
    tag = (message.text or "").strip()
    if not tag:
        return await dm.show()

    user_id = get_user_id(dm)

    USER_TAGS.setdefault(user_id, [])

    if tag not in USER_TAGS[user_id]:
        USER_TAGS[user_id].append(tag)

    dm.dialog_data["tag"] = tag

    await dm.switch_to(PanelSG.announcement_title)


# =========================
# FLOW INPUT
# =========================

async def on_title_success(message: Message, widget, dm: DialogManager):
    dm.dialog_data["title"] = (message.text or "").strip()
    await dm.next()


async def on_content_success(message: Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    if not text:
        return await dm.show()

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    await dm.next()


# =========================
# SEND
# =========================

async def send_announcement(callback: CallbackQuery, button, dm: DialogManager):
    data = d(dm)

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        await callback.answer("Config error", show_alert=True)
        return

    caption = (
        f"📣 <b>{data.get('title') or 'Announcement'}</b>\n\n"
        f"{data.get('content')}\n\n"
        f"────────────\n"
        f"🏷 {data.get('tag')}\n"
        f"👤 {resolve_sender(dm)}"
    )

    for chat_id in config.access.chat_ids:
        await bot.send_message(chat_id, caption)

    await callback.answer("Sent")
    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 Announcement Creator"),
    Row(
        Button(Const("📣 Create"), id="start", on_click=to_announcement_menu)
    ),
    state=PanelSG.main,
)


announcement_menu_window = Window(
    Format(
        "📣 <b>Announcement Creator</b>\n\n"
        "Select tag (page {page})"
    ),
    Select(
        Format("• {item}"),
        id="tag_select",
        items="tags",
        item_id_getter=lambda x: x,
        on_click=select_tag,
    ),
    Row(
        Button(Const("⬅"), id="prev", on_click=prev_page, when="has_prev"),
        Button(Const("➡"), id="next", on_click=next_page, when="has_next"),
    ),
    Row(
        Button(Const("➕ Create tag"), id="create_tag", on_click=to_create_tag),
    ),
    getter=tags_getter,
    state=PanelSG.announcement_menu,
)


create_tag_window = Window(
    Const("📣 <b>Announcement Creator</b>\n\n✍️ Type new tag"),
    MessageInput(create_tag_input),
    state=PanelSG.create_tag,
)


title_window = Window(
    Format(
        "📣 <b>Announcement Creator</b>\n\n"
        "🏷 {tag}\n\n"
        "Give title (or skip)"
    ),
    MessageInput(on_title_success),
    Row(Button(Const("➡ Skip"), id="skip", on_click=next_to_content)),
    getter=title_getter,
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("📣 <b>Announcement Creator</b>\n\n✍️ Write message"),
    MessageInput(on_content_success),
    Row(Button(Const("⬅ Back"), id="back", on_click=back_to_title)),
    state=PanelSG.announcement_content,
)


preview_window = Window(
    Format(
        "📣 <b>{title}</b>\n\n"
        "{content}\n\n"
        "────────────\n"
        "🏷 {tag}\n"
        "👤 {sender}"
    ),
    Row(
        Button(Const("⬅ Edit"), id="edit", on_click=back_to_title),
        Button(Const("🚀 Send"), id="send", on_click=send_announcement),
    ),
    getter=preview_getter,
    state=PanelSG.announcement_preview,
)


panel_dialog = Dialog(
    main_window,
    announcement_menu_window,
    create_tag_window,
    title_window,
    content_window,
    preview_window,
)