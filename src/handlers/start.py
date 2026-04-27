# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Bot entry point → starts announcement flow
# =========================================

import logging

from aiogram import Router, types
from aiogram.filters import CommandStart

from src.flows.announcement_flow import start_flow

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user

    if user is None:
        logger.warning("[START] missing user")
        return

    logger.info(f"[START] user_id={user.id} starting flow")

    await start_flow(message)