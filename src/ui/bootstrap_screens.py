# src/ui/bootstrap_screens.py

import logging

from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_middleware import ScreenMiddlewareManager, InjectUserMiddleware
from src.ui.screen_engine import ScreenEngine

from src.ui.screens.home.r3_home_screen import render_r3_home_screen

logger = logging.getLogger("shadow.ui.bootstrap")


def build_screen_system():
    logger.info("[BOOTSTRAP] init screen system")

    registry = ScreenRegistry()

    # =========================
    # R3 TEST ONLY
    # =========================
    registry.register("home", render_r3_home_screen)

    middleware = ScreenMiddlewareManager()
    middleware.add(InjectUserMiddleware())

    engine = ScreenEngine(registry, middleware)

    logger.info("[BOOTSTRAP] screen system ready")

    return registry, middleware, engine


# =========================================================
# COMPAT LAYER (USED BY bot.py)
# =========================================================

def register_screens(registry: ScreenRegistry):
    """
    Compatibility layer for bot.py bootstrap.

    bot.py expects:
        register_screens(registry)
    """

    logger.info("[BOOTSTRAP] register_screens() called")

    registry.register("home", render_r3_home_screen)