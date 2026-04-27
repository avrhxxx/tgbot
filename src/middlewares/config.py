# =========================================
# FILE: src/middlewares/config.py
# DESCRIPTION:
# Injects config into aiogram middleware context
# =========================================

import logging

logger = logging.getLogger(__name__)


class ConfigMiddleware:
    def __init__(self, config):
        self.config = config

    async def __call__(self, handler, event, data):
        data["config"] = self.config
        return await handler(event, data)