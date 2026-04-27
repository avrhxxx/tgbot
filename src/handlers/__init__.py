# =========================================
# GROUP: handlers
# FILE: __init__.py
# DESCRIPTION:
# Router aggregation
# =========================================

from .start import router as start_router



def register_handlers(dp):
    dp.include_router(start_router)
  
