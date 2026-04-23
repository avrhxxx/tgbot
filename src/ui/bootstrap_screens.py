# src/ui/bootstrap_screens.py

from src.ui.screen_registry import ScreenRegistry

from src.ui.screens.home_screen import render_home_screen
from src.ui.screens.events_screen import render_events_screen
from src.ui.screens.settings_screen import render_settings_screen


def register_screens(registry: ScreenRegistry):
    registry.register("home", render_home_screen)
    registry.register("events", render_events_screen)
    registry.register("settings", render_settings_screen)