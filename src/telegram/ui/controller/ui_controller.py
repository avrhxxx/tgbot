# =========================================
# GROUP: telegram.ui.controller
# FILE: ui_controller.py
# =========================================

import logging
from aiogram_dialog import DialogManager

from src.telegram.states.home import HomeSG, SettingsSG

logger = logging.getLogger(__name__)


class UIController:
    """
    Central UI switcher.
    No routing logic elsewhere.
    """

    def __init__(self):
        self.map = {
            "home": HomeSG.main,
            "settings": SettingsSG.main,
        }

    async def switch(self, route: str, dialog_manager: DialogManager):
        state = self.map.get(route)

        if not state:
            logger.warning("Unknown route: %s", route)
            return

        logger.info("UI switch | route=%s state=%s", route, state)

        await dialog_manager.switch_to(state)


ui_controller = UIController()