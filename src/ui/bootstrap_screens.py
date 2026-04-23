# src/ui/bootstrap_screens.py

import logging

from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_middleware import ScreenMiddlewareManager, InjectUserMiddleware
from src.ui.screen_engine import ScreenEngine

from src.ui.screens.home_screen import build_home_screen
from src.ui.screens.events_screen import render_events_screen
from src.ui.screens.settings_screen import render_settings_screen

logger = logging.getLogger("shadow.ui.bootstrap")


def build_screen_system():

    logger.info("[BOOTSTRAP] init screen system")

    registry = ScreenRegistry()

    registry.register("home", build_home_screen)
    registry.register("events", render_events_screen)
    registry.register("settings", render_settings_screen)

    middleware = ScreenMiddlewareManager()
    middleware.add(InjectUserMiddleware())

    engine = ScreenEngine(registry, middleware)

    logger.info("[BOOTSTRAP] screen system ready")

    return registry, middleware, engine