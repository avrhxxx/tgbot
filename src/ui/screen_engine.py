# src/ui/screen_engine.py

"""
Core UI Engine:
- registry execution
- middleware pipeline
- screen stack (BACK system)
"""

import logging
from collections import defaultdict
from typing import Any

from src.ui.screen_contracts import ScreenResult

logger = logging.getLogger("shadow.ui.engine")


class ScreenEngine:
    """
    CORE UI ENGINE:
    - registry execution
    - middleware pipeline
    - screen stack (BACK system)
    """

    def __init__(self, registry, middleware):
        self.registry = registry
        self.middleware = middleware

        # user_id → stack
        self._stack: dict[str, list[str]] = defaultdict(list)

    # =========================
    # STACK OPS
    # =========================
    def push(self, user_id: str, screen_id: str) -> None:
        self._stack[user_id].append(screen_id)
        logger.info(f"[STACK] push {user_id} → {screen_id}")

    def pop(self, user_id: str) -> str | None:
        if not self._stack[user_id]:
            return None

        self._stack[user_id].pop()

        if not self._stack[user_id]:
            return None

        previous = self._stack[user_id][-1]
        logger.info(f"[STACK] pop → {previous}")
        return previous

    def current(self, user_id: str) -> str | None:
        if not self._stack[user_id]:
            return None
        return self._stack[user_id][-1]

    # =========================
    # MAIN PIPELINE
    # =========================
    async def render(
        self,
        screen_id: str,
        **context: Any,
    ) -> ScreenResult:
        user_id = context.get("user_id")

        logger.info(f"[ENGINE] render {screen_id} user={user_id}")

        if isinstance(user_id, str):
            self.push(user_id, screen_id)

        # middleware pre
        context = await self.middleware.run_before(screen_id, context)

        # registry render
        result: ScreenResult = await self.registry.render(
            screen_id,
            **context,
        )

        # middleware post
        result = await self.middleware.run_after(
            screen_id,
            context,
            result,
        )

        return result