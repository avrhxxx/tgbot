# src/telegram/handlers/events.py
# =========================================
# GROUP: telegram.handlers
# FILE: events.py
# DESCRIPTION:
# Event system entry router.
# Will handle Event List Window + Event Detail Windows.
# =========================================

from aiogram import Router

router = Router()

# FUTURE:
# - event list (dynamic buttons)
# - event detail window
# - reservoir/open logic (backend hidden)
# - actions per event stage