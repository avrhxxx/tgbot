# =========================================
# GROUP: telegram.permissions
# FILE: context_builder.py
# DESCRIPTION:
# Builds UserContext from Telegram update/user.
# Central identity resolver for routing system.
# =========================================

import logging
from typing import Optional

from aiogram.types import User as TgUser

from src.telegram.permissions.context import UserContext
from src.telegram.permissions.roles import Role

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Converts Telegram user into internal UserContext.
    """

    def __init__(self):
        logger.info("ContextBuilder initialized")

    async def build(self, tg_user: TgUser) -> UserContext:
        """
        Resolve user role and build context.
        """

        user_id = tg_user.id

        # -------------------------------------------------
        # TEMP MOCK (later: DB / Redis / API)
        # -------------------------------------------------
        role = await self._resolve_role(user_id)

        context = UserContext(
            user_id=user_id,
            role=role,
        )

        logger.info(
            "UserContext built | user_id=%s role=%s",
            user_id,
            role,
        )

        return context

    async def _resolve_role(self, user_id: int) -> Role:
        """
        Temporary role resolver.
        Replace later with DB / external service.
        """

        # 🔥 TEMP LOGIC (safe default)
        # later: database lookup, alliance membership, admin table

        if user_id == 1:
            return Role.OWNER

        return Role.R3


# global instance
context_builder = ContextBuilder()