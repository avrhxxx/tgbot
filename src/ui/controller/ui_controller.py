# =========================================
# GROUP: ui.controller
# FILE: ui_controller.py
# =========================================

import logging

from src.ui.state.ui_state import UIState
from src.ui.renderer.message_renderer import render_screen

logger = logging.getLogger(__name__)


class UIController:
    def __init__(self, bot):
        self.bot = bot
        self.state = UIState()

    async def open_screen(self, chat_id: int, screen: str):
        self.state.screen = screen

        text, keyboard = await render_screen(screen, chat_id)

        if self.state.message_id:
            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=self.state.message_id,
                text=text,
                reply_markup=keyboard,
            )
        else:
            msg = await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
            )
            self.state.message_id = msg.message_id