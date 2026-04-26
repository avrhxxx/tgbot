# src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel dialog with broadcast input flow.

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput

from src.dialogs.panel.states import PanelSG


# =========================
# CALLBACKS
# =========================

async def on_broadcast_click(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.broadcast_input)


async def on_settings_click(callback, button, dialog_manager: DialogManager):
    await callback.answer("🚧 Settings coming soon")


async def on_broadcast_message(message, widget, dialog_manager: DialogManager):
    await message.answer("📩 Got message (next step: preview)")


# =========================
# WINDOWS
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

broadcast_input_window = Window(
    Const("📣 <b>Send broadcast message:</b>\n\nType your message below."),
    MessageInput(on_broadcast_message),
    state=PanelSG.broadcast_input,
)


# =========================
# DIALOG
# =========================

panel_dialog = Dialog(
    main_window,
    broadcast_input_window,
)