# =========================================
# GROUP: services.user
# FILE: context_store.py
# DESCRIPTION:
# Runtime UserContext storage for routing system.
# Fix for aiogram-dialog callback context loss.
# =========================================

import logging
from typing import Dict, Optional

from src.telegram.permissions.context import UserContext

logger = logging.getLogger(__name__)


class UserContextStore:
    """
    Simple in-memory runtime storage for UserContext.
    Used because aiogram-dialog callbacks do NOT reliably
    preserve middleware_data across click routing.
    """

    def __init__(self):
        self._storage: Dict[int, UserContext] = {}

        logger.info("UserContextStore initialized")

    def set(self, user_id: int, context: UserContext) -> None:
        self._storage[user_id] = context

        logger.info(
            "UserContext stored | user_id=%s role=%s",
            user_id,
            context.role,
        )

    def get(self, user_id: int) -> Optional[UserContext]:
        return self._storage.get(user_id)


# global instance
user_context_store = UserContextStore()