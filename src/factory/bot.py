# src/factory/bot.py
# =========================================
# GROUP: factory
# FILE: bot.py
# DESCRIPTION:
# Creates and configures Aiogram Bot instance.
# Production-ready setup with config integration.
# =========================================

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import LinkPreviewOptions

from src.config.config import load_config


def create_bot() -> Bot:
    """
    Creates configured Telegram Bot instance.
    """
    config = load_config()

    return Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(
            parse_mode="HTML",
            link_preview=LinkPreviewOptions(is_disabled=True),
        ),
    )