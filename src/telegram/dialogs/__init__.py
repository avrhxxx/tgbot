# =========================================
# GROUP: telegram.dialogs
# FILE: __init__.py
# DESCRIPTION:
# Dialog system bootstrap entry.
# Uses aiogram-dialog auto discovery via setup_dialogs.
# =========================================

import logging
from aiogram_dialog import setup_dialogs

logger = logging.getLogger(__name__)


def setup_all_dialogs(dp) -> None:
    """
    Initializes aiogram-dialog system.

    NOTE:
    Dialogs are now registered via include_router(Dialog(...))
    in factory layer, not imported manually here.
    """

    logger.info("Setting up aiogram-dialog system...")
    setup_dialogs(dp)
    logger.info("aiogram-dialog setup completed")