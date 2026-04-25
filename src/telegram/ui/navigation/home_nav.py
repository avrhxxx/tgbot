# =========================================
# GROUP: telegram.ui.navigation
# FILE: home_nav.py
# DESCRIPTION:
# UI navigation layer (aiogram_dialog ONLY)
# Responsible only for switching dialogs.
# =========================================

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from src.telegram.states.home import HomeSG, EventsSG, SettingsSG, HelpSG


async def navigate(route: str, manager: DialogManager):

    match route:
        case "home":
            await manager.switch_to(HomeSG.main)

        case "events":
            await manager.switch_to(EventsSG.main)

        case "settings":
            await manager.switch_to(SettingsSG.main)

        case "help":
            await manager.switch_to(HelpSG.main)