import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import SettingsSG

logger = logging.getLogger(__name__)


settings_window = Window(
    Format(
        "⚙️ Settings\n\nUser preferences coming soon."
    ),
    Row(
        Button(Format("⬅️ Back"), id="back"),
    ),
    state=SettingsSG.main,
)