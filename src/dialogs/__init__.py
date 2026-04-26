# src/dialogs/__init__.py
# DESCRIPTION:
# Registers all dialogs.

from aiogram_dialog import setup_dialogs

from src.dialogs.panel.dialog import panel_dialog


def register_dialogs(dp):
    dp.include_router(panel_dialog)
    setup_dialogs(dp)