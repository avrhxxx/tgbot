# src/dialogs/panel/dialog.py

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row

from src.dialogs.panel.states import PanelSG


# =========================
# NAVIGATION
# =========================

async def to_broadcast_menu(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.broadcast_menu)


async def back_to_main(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.main)


# =========================
# WINDOWS
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>\n\nChoose an action:"),
    Row(
        Button(Const("📣 Broadcast"), id="broadcast", on_click=to_broadcast_menu),
    ),
    Row(
        Button(Const("⚙️ Settings"), id="settings"),
    ),
    state=PanelSG.main,
)

broadcast_menu_window = Window(
    Const("📣 <b>Broadcast Menu</b>\n\nChoose action:"),
    Row(
        Button(Const("➕ Create Broadcast"), id="create_broadcast"),
    ),
    Row(
        Button(Const("⬅ Back"), id="back", on_click=back_to_main),
    ),
    state=PanelSG.broadcast_menu,
)


# =========================
# DIALOG
# =========================

panel_dialog = Dialog(
    main_window,
    broadcast_menu_window,
)