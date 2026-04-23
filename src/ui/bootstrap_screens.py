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
# COMPAT LAYER (FIX FOR BOT IMPORT EXPECTATION)
# =========================================================

_registry = None
_middleware = None
_engine = None


def register_screens():
    """
    Legacy compatibility for bootstrap entrypoints expecting:
    register_screens()
    """

    global _registry, _middleware, _engine

    logger.info("[BOOTSTRAP] register_screens() called")

    _registry, _middleware, _engine = build_screen_system()

    return _registry, _middleware, _engine


def get_screen_system():
    """
    Optional accessor for app/bootstrap layer
    """
    if _registry is None:
        return build_screen_system()
    return _registry, _middleware, _engine