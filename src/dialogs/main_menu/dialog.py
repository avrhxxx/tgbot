# =========================================
# FILE: src/dialogs/main_menu/dialog.py
# DESCRIPTION:
# Main Menu Dialog (UI hub for all bot flows)
# =========================================

import logging
from datetime import datetime

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row

from src.dialogs.main_menu.states import MainMenuSG

logger = logging.getLogger(__name__)


# =========================
# SAFE USER RESOLVE
# =========================

def get_user(dm: DialogManager):
    event = dm.event

    if isinstance(event, Message):
        return event.from_user
    if isinstance(event, CallbackQuery):
        return event.from_user

    return None


# =========================
# GETTER
# =========================

async def main_menu_getter(dialog_manager: DialogManager, **kwargs):
    user = get_user(dialog_manager)

    return {
        "username": user.first_name if user else "User",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    }


# =========================
# WINDOWS
# =========================

main_menu_window = Window(
    Format(
        "MAIN MENU\n\n"
        "Welcome, {username}\n"
        "Date: {date}\n\n"
        "Choose an option:"
    ),
    Row(
        Button(
            Const("📢 Group Message"),
            id="group_message",
            on_click=lambda c, b, m: m.switch_to(MainMenuSG.group_message),
        )
    ),
    Row(
        Button(
            Const("📅 Event Manager"),
            id="events",
            on_click=lambda c, b, m: m.switch_to(MainMenuSG.event_manager),
        )
    ),
    Row(
        Button(
            Const("🌐 Language"),
            id="language",
            on_click=lambda c, b, m: m.switch_to(MainMenuSG.language),
        )
    ),
    state=MainMenuSG.main,
    getter=main_menu_getter,
)


# =========================
# DIALOG
# =========================

main_menu_dialog = Dialog(
    main_menu_window
)