# =========================================
# GROUP: handlers
# FILE: __init__.py
# DESCRIPTION:
# Router aggregation
# =========================================

from .start import router as start_router
from .broadcast import router as broadcast_router


def register_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(broadcast_router)