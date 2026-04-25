# =========================================
# GROUP: telegram.ui.windows
# FILE: registry.py
# =========================================

from src.telegram.ui.windows.home_window import home_window
from src.telegram.ui.windows.settings_window import settings_window


def get_windows():
    return [
        home_window,
        settings_window,
    ]