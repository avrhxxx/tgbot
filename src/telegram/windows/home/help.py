import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HelpSG

logger = logging.getLogger(__name__)


help_window = Window(
    Format(
        "❓ Help\n\nFAQ / support coming soon."
    ),
    Row(
        Button(Format("⬅️ Back"), id="back"),
    ),
    state=HelpSG.main,
)