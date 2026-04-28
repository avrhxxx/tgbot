import logging
from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.event_manager.states import EventManagerSG
from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


# =========================
# EVENT TYPES (safe ids)
# =========================

EVENT_TYPES = {
    "arcadian": "Arcadian Conquest",
    "ghoulion": "Ghoulion Pursuit",
    "reservoir": "Reservoir Raid",
    "kvk": "KvK",
    "city": "City Contest",
}


# =========================
# DATE GENERATOR
# =========================

def generate_dates(days: int = 7):
    base = datetime.utcnow().date()
    return [(base + timedelta(days=i)).isoformat() for i in range(days)]


# =========================
# TYPE HANDLER
# =========================

async def on_type_select(callback: CallbackQuery, button, dm: DialogManager):
    key = button.widget_id
    dm.dialog_data["type"] = EVENT_TYPES.get(key)

    logger.info(f"[EVENT] type set -> {key}")

    await dm.switch_to(EventManagerSG.date)


# =========================
# DATE HANDLER
# =========================

async def on_date_select(callback: CallbackQuery, button, dm: DialogManager):
    date_map = dm.dialog_data.get("date_map", {})

    selected = date_map.get(button.widget_id)

    dm.dialog_data["date"] = selected

    logger.info(f"[EVENT] date set -> {selected}")

    await dm.switch_to(EventManagerSG.time)


# =========================
# TIME HANDLER
# =========================

async def on_time_input(message: Message, widget, dm: DialogManager):
    time = (message.text or "").strip()

    if not time:
        return

    dm.dialog_data["time"] = time

    logger.info(f"[EVENT] time set -> {time}")

    await dm.switch_to(EventManagerSG.description)


# =========================
# DESCRIPTION HANDLER
# =========================

async def on_description(message: Message, widget, dm: DialogManager):
    text = (message.text or "").strip()

    dm.dialog_data["description"] = text or None

    logger.info("[EVENT] description set")

    await dm.switch_to(EventManagerSG.preview)


async def skip_description(callback: CallbackQuery, button, dm: DialogManager):
    dm.dialog_data["description"] = None

    logger.info("[EVENT] description skipped")

    await dm.switch_to(EventManagerSG.preview)


# =========================
# DATE GETTER (IMPORTANT)
# =========================

async def date_getter(dialog_manager: DialogManager, **kwargs):
    dates = generate_dates(7)

    date_map = {f"d{i}": d for i, d in enumerate(dates)}

    dialog_manager.dialog_data["date_map"] = date_map

    return {
        "dates": [(k, v) for k, v in date_map.items()]
    }


# =========================
# PREVIEW GETTER
# =========================

async def preview_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data

    return {
        "type": data.get("type"),
        "date": data.get("date"),
        "time": data.get("time"),
        "description": data.get("description") or "-",
    }


# =========================
# SEND EVENT
# =========================

async def on_send(callback: CallbackQuery, button, dm: DialogManager):
    config = dm.middleware_data.get("config")
    bot = dm.middleware_data.get("bot")

    if not config or not bot:
        await callback.answer("Missing bot/config", show_alert=True)
        return

    text = (
        "EVENT\n"
        "━━━━━━━━━━━━━━\n"
        f"Type: {dm.dialog_data.get('type')}\n"
        f"Date: {dm.dialog_data.get('date')}\n"
        f"Time (UTC): {dm.dialog_data.get('time')}\n\n"
        "Description:\n"
        f"{dm.dialog_data.get('description') or '-'}\n"
        "━━━━━━━━━━━━━━"
    )

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"[EVENT] send failed {chat_id}: {e}")

    await callback.answer("Event sent ✔")

    await dm.start(MainMenuSG.main, mode=StartMode.RESET_STACK)


# =========================
# WINDOWS
# =========================

# -------- TYPE --------
type_window = Window(
    Const("Select event type:"),
    Row(*[
        Button(Const(label), id=key, on_click=on_type_select)
        for key, label in EVENT_TYPES.items()
    ]),
    state=EventManagerSG.type,
)

# -------- DATE --------
date_window = Window(
    Const("Select date (next 7 days):"),
    Row(*[
        Button(Format("{item[1]}"), id="{item[0]}", on_click=on_date_select)
    ]),
    getter=date_getter,
    state=EventManagerSG.date,
)

# -------- TIME --------
time_window = Window(
    Const("Enter time (UTC) HH:MM:"),
    MessageInput(on_time_input),
    state=EventManagerSG.time,
)

# -------- DESCRIPTION --------
desc_window = Window(
    Const("Enter description (optional):"),
    MessageInput(on_description),
    Row(
        Button(Const("Skip"), id="skip", on_click=skip_description),
    ),
    state=EventManagerSG.description,
)

# -------- PREVIEW --------
preview_window = Window(
    Format(
        "EVENT\n"
        "━━━━━━━━━━━━━━\n"
        "Type: {type}\n"
        "Date: {date}\n"
        "Time (UTC): {time}\n\n"
        "Description:\n{description}\n"
        "━━━━━━━━━━━━━━"
    ),
    Row(
        Button(Const("Send"), id="send", on_click=on_send),
    ),
    Row(
        Button(Const("Back"), id="back", on_click=lambda c, b, m: m.back()),
    ),
    getter=preview_getter,
    state=EventManagerSG.preview,
)


# =========================
# DIALOG
# =========================

event_manager_dialog = Dialog(
    type_window,
    date_window,
    time_window,
    desc_window,
    preview_window,
)