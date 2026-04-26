# src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel dialog (main window only).

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row

from src.dialogs.panel.states import PanelSG


# =========================
# HANDLERS (na razie puste)
# =========================

async def on_broadcast_click(callback, button, dialog_manager: DialogManager):
    await callback.answer("🚧 Broadcast flow coming soon")


async def on_settings_click(callback, button, dialog_manager: DialogManager):
    await callback.answer("🚧 Settings coming soon")


# =========================
# WINDOW
# =========================

main_window = Window(
    Const("🛠 <b>Moderator Panel</b>\n\nChoose an action:"),
    Row(
        Button(Const("📣 Create Broadcast"), id="broadcast", on_click=on_broadcast_click),
    ),
    Row(
        Button(Const("⚙️ Settings"), id="settings", on_click=on_settings_click),
    ),
    state=PanelSG.main,
)


# =========================
# DIALOG
# =========================

panel_dialog = Dialog(main_window)