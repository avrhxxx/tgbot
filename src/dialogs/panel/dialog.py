# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v7.1
# (pure dialog UX + callback toasts + dynamic tags)
# =========================================

import logging
from typing import Optional, Tuple, List

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Select
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG

logger = logging.getLogger(__name__)


# =========================
# IN-MEMORY TAG STORAGE
# =========================

TAGS: List[str] = []


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


def trace(dm: DialogManager, label: str):
    try:
        state = dm.current_context().state
        state_repr = getattr(state, "state", str(state))
    except Exception:
        state_repr = "UNKNOWN"

    logger.info(f"[ANNOUNCEMENT] {label} | state={state_repr} | data={dm.dialog_data}")


# =========================
# GETTERS
# =========================

async def tags_getter(**_):
    return {"tags": TAGS}


async def preview_getter(dm: DialogManager, **_):
    data = d(dm)
    return {
        "title": data.get("title") or "Announcement",
        "content": data.get("content") or "",
        "tag": data.get("tag") or "unknown",
        "sender": resolve_sender(dm),
    }


# =========================
# NAVIGATION
# =========================

async def to_announcement_menu(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    trace(dm, "START")
    await dm.switch_to(PanelSG.announcement_menu)


async def back_to_main(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    trace(dm, "EXIT")
    await dm.switch_to(PanelSG.main)


async def next_to_content(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_content)


async def back_to_title(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer()
    await dm.switch_to(PanelSG.announcement_title)


async def to_create_tag(callback: CallbackQuery, button, dm: DialogManager):
    await callback.answer("Enter new tag name…")
    trace(dm, "CREATE TAG")
    await dm.switch_to(PanelSG.create_tag)


# =========================
# TAG HANDLING
# =========================

async def select_tag(callback: CallbackQuery, widget, dm: DialogManager, item_id: str):
    dm.dialog_data["tag"] = item_id
    trace(dm, f"TAG={item_id}")

    await callback.answer(f"Selected: {item_id}")
    await dm.switch_to(PanelSG.announcement_title)


async def create_tag_input(message: Message, widget, dm: DialogManager):
    tag = (message.text or "").strip()

    if not tag:
        return await dm.show()

    if tag not in TAGS:
        TAGS.append(tag)

    dm.dialog_data["tag"] = tag
    trace(dm, f"TAG CREATED={tag}")

    # toast via last callback (hack: fallback to show)
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

    trace(dm, "TO PREVIEW")
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
        return await dm.switch_to(PanelSG.main)

    caption = (
        f"📣 <b>{data.get('title') or 'Announcement'}</b>\n\n"
        f"{data.get('content')}\n\n"
        f"────────────\n"
        f"🏷 {data.get('tag')}\n"
        f"👤 {resolve_sender(dm)}"
    )

    for chat_id in config.access.chat_ids:
        await bot.send_message(chat_id, caption)

    await callback.answer("Sent!", show_alert=False)
    trace(dm, "SENT")

    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 Moderator Panel"),
    Row(
        Button(Const("📣 Create announcement"), id="start", on_click=to_announcement_menu)
    ),
    state=PanelSG.main,
)


announcement_menu_window = Window(
    Const("📣 choose or create a tag"),
    Select(
        Format("• {item}"),
        id="tag_select",
        items="tags",
        item_id_getter=lambda x: x,
        on_click=select_tag,
    ),
    Row(
        Button(Const("➕ Create tag"), id="create_tag", on_click=to_create_tag),
    ),
    getter=tags_getter,
    state=PanelSG.announcement_menu,
)


create_tag_window = Window(
    Const("✍️ type new tag name"),
    MessageInput(create_tag_input),
    state=PanelSG.create_tag,
)


title_window = Window(
    Format(
        "📝 tag: {tag}\n\n"
        "give title (or skip)"
    ),
    MessageInput(on_title_success),
    Row(Button(Const("➡ Skip"), id="skip_title", on_click=next_to_content)),
    getter=lambda dm, **_: {"tag": d(dm).get("tag", "unknown")},
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("✍️ write message"),
    MessageInput(on_content_success),
    Row(Button(Const("⬅ Back"), id="back_content", on_click=back_to_title)),
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
        Button(Const("⬅ Edit"), id="back_preview", on_click=back_to_title),
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