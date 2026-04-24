import logging
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

logger = logging.getLogger(__name__)


settings_window = Window(
    Format(
        "⚙️ Settings\n\nUser preferences coming soon."
    ),
    Row(Button(Format("⬅️ Back"), id="home")),
)