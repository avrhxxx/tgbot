# src/dialogs/panel/dialog.py
# DESCRIPTION:
# Moderator panel dialog with navigation.

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram.types import Message

from src.dialogs.panel.states import PanelSG


# =========================
# HANDLERS
# =========================

async def on_broadcast_click(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(PanelSG.broadcast_input)


async def on_settings_click(callback, button, dialog_manager: DialogManager):
    await callback.answer("🚧 Settings coming soon")


# =========================
# INPUT HANDLER
# =========================

async def on_message(message: Message, dialog_manager: DialogManager):
    await message.answer("📩 Got your message (next step soon)")


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
    Const("📣 <b>Send broadcast message:</b>\n\nJust type your message."),
    state=PanelSG.broadcast_input,
)


# =========================
# DIALOG
# =========================

panel_dialog = Dialog(
    main_window,
    broadcast_input_window,
    on_message=on_message,
)