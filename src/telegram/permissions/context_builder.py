# =========================================
# GROUP: telegram.permissions
# FILE: context_builder.py
# DESCRIPTION:
# Builds unified UserContext from UserProfileService.
# SINGLE SOURCE OF TRUTH for user identity + role.
# =========================================

import logging

from src.services.user.user_profile import user_profile
from src.telegram.permissions.context import UserContext

logger = logging.getLogger(__name__)


class ContextBuilder:

    async def build(self, tg_user) -> UserContext:
        """
        Always builds context from UserProfileService.
        No FSM / middleware dependency.
        """

        user_id = tg_user.id

        profile = user_profile.get(user_id)

        if not profile:
            # fallback safe state
            profile = user_profile.create_or_update(
                user_id=user_id,
                nickname=tg_user.username or tg_user.first_name or "User",
            )

        context = UserContext(
            user_id=user_id,
            role=profile.role,
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