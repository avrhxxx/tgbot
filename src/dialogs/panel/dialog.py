# =========================================
# FILE: src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel + announcement wizard v7.0
# (single-message UX + dynamic tags + create tag + clean dialog flow)
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
# SIMPLE IN-MEMORY TAG STORAGE
# =========================

TAGS: List[str] = ["Tag1", "Tag2"]


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
    return {
        "tags": TAGS
    }


async def preview_getter(dm: DialogManager, **_):
    return {
        "title": d(dm).get("title") or "Announcement",
        "content": d(dm).get("content") or "",
        "tag": d(dm).get("tag") or "unknown",
        "sender": resolve_sender(dm),
    }


# =========================
# NAVIGATION
# =========================

async def to_announcement_menu(callback, button, dm: DialogManager):
    trace(dm, "START")
    await dm.switch_to(PanelSG.announcement_menu)


async def back_to_main(callback, button, dm: DialogManager):
    trace(dm, "EXIT")
    await dm.switch_to(PanelSG.main)


async def next_to_content(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.announcement_content)


async def back_to_title(callback, button, dm: DialogManager):
    await dm.switch_to(PanelSG.announcement_title)


async def to_create_tag(callback, button, dm: DialogManager):
    trace(dm, "CREATE TAG")
    await dm.switch_to(PanelSG.create_tag)


# =========================
# TAG HANDLING
# =========================

async def select_tag(callback: CallbackQuery, widget, dm: DialogManager, item_id: str):
    dm.dialog_data["tag"] = item_id
    trace(dm, f"TAG={item_id}")
    await dm.switch_to(PanelSG.announcement_title)


async def create_tag_input(message: Message, widget, dm: DialogManager):
    tag = (message.text or "").strip()

    if not tag:
        await dm.show()
        return

    if tag not in TAGS:
        TAGS.append(tag)

    dm.dialog_data["tag"] = tag
    trace(dm, f"TAG CREATED={tag}")

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
        await dm.show()
        return

    dm.dialog_data["content"] = text
    dm.dialog_data["media"] = save_media(message)

    trace(dm, "TO PREVIEW")
    await dm.next()


# =========================
# SEND
# =========================

async def send_announcement(callback, button, dm: DialogManager):
    data = d(dm)

    bot = dm.middleware_data.get("bot")
    config = dm.middleware_data.get("config")

    if not bot or not config:
        return await dm.switch_to(PanelSG.main)

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
            logger.warning(f"[ANNOUNCEMENT] failed chat_id={chat_id}: {e}")

    trace(dm, "SENT")
    await dm.switch_to(PanelSG.main)


# =========================
# WINDOWS (SINGLE MESSAGE UX)
# =========================

main_window = Window(
    Const("🛠 Moderator Panel"),
    Row(
        Button(Const("📣 Create announcement"), id="announcement", on_click=to_announcement_menu)
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
        "give your announcement a title\n"
        "(or skip)"
    ),
    MessageInput(on_title_success),
    Row(Button(Const("➡ Skip"), id="skip_title", on_click=next_to_content)),
    getter=lambda dm, **_: {"tag": d(dm).get("tag", "unknown")},
    state=PanelSG.announcement_title,
)


content_window = Window(
    Const("✍️ now write your message"),
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