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
# EVENT TYPES (fixed set)
# =========================

EVENT_TYPES = [
    "Arcadian Conquest",
    "Ghoulion Pursuit",
    "Reservoir Raid",
    "KvK",
    "City Contest",
]


# =========================
# DATE GENERATOR (7 days)
# =========================

def generate_dates(days: int = 7):
    base = datetime.utcnow().date()
    return [(base + timedelta(days=i)).isoformat() for i in range(days)]


# =========================
# TYPE HANDLER
# =========================

async def on_type_select(callback: CallbackQuery, button, dm: DialogManager):
    index = int(button.widget_id.replace("t", ""))
    selected = EVENT_TYPES[index]

    dm.dialog_data["type"] = selected
    logger.info(f"[EVENT] type set -> {selected}")

    await dm.switch_to(EventManagerSG.date)


# =========================
# DATE HANDLER
# =========================

async def on_date_select(callback: CallbackQuery, button, dm: DialogManager):
    dates = generate_dates(7)

    index = int(button.widget_id.replace("d", ""))
    selected = dates[index]

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
        f"EVENT\n"
        f"━━━━━━━━━━━━━━\n"
        f"Type: {dm.dialog_data.get('type')}\n"
        f"Date: {dm.dialog_data.get('date')}\n"
        f"Time (UTC): {dm.dialog_data.get('time')}\n\n"
        f"Description:\n{dm.dialog_data.get('description') or '-'}\n"
        f"━━━━━━━━━━━━━━"
    )

    for chat_id in config.access.chat_ids:
        try:
            await bot.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"[EVENT] send failed {chat_id}: {e}")

    await callback.answer("Event sent ✔")

    await dm.start(MainMenuSG.main, mode=StartMode.RESET_STACK)


# =========================
# BUILD BUTTONS
# =========================

def build_type_buttons():
    return Row(*[
        Button(Const(t), id=f"t{i}", on_click=on_type_select)
        for i, t in enumerate(EVENT_TYPES)
    ])


def build_date_buttons():
    dates = generate_dates(7)

    return Row(*[
        Button(Const(d), id=f"d{i}", on_click=on_date_select)
        for i, d in enumerate(dates)
    ])


# =========================
# WINDOWS
# =========================

# -------- TYPE --------
type_window = Window(
    Const("Select event type:"),
    build_type_buttons(),
    state=EventManagerSG.type,
)

# -------- DATE --------
date_window = Window(
    Const("Select date (next 7 days):"),
    build_date_buttons(),
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