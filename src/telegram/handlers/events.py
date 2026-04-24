# =========================================
# GROUP: telegram.handlers
# FILE: events.py
# DESCRIPTION:
# Event system entry router.
# Will handle Event List Window + Event Detail Windows.
# =========================================

import logging

from aiogram import Router

logger = logging.getLogger(__name__)

router = Router()

logger.info("Events router initialized")

# FUTURE:
# - event list (dynamic buttons)
# - event detail window
# - reservoir/open logic (backend hidden)
# - actions per event stage