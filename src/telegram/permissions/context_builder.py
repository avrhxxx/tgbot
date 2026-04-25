# =========================================
# GROUP: telegram.permissions
# FILE: context_builder.py
# =========================================

import logging

from src.services.user.user_profile import user_profile
from src.telegram.permissions.context import UserContext
from src.telegram.permissions.roles import Role

logger = logging.getLogger(__name__)


class ContextBuilder:

    async def build(self, tg_user) -> UserContext:

        user_id = tg_user.id

        profile = user_profile.get(user_id)

        if not profile:
            profile = user_profile.create_or_update(
                user_id=user_id,
                nickname=tg_user.username or tg_user.first_name or "User",
            )

        context = UserContext(
            user_id=user_id,
            role=Role(profile.role),  # 🔥 FIX STR → ENUM
            nickname=profile.nickname,
            username=tg_user.username,
            first_name=tg_user.first_name,
        )

        logger.info(
            "UserContext built | user_id=%s role=%s",
            user_id,
            context.role,
        )

        return context


context_builder = ContextBuilder()