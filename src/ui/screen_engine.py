# src/ui/screen_engine.py

import logging
from collections import defaultdict
from typing import Dict, List, Any, Optional

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
        self._stack: Dict[str, List[str]] = defaultdict(list)

    # =========================
    # STACK OPS
    # =========================
    def push(self, user_id: str, screen_id: str) -> None:
        self._stack[user_id].append(screen_id)
        logger.info(f"[STACK] push {user_id} → {screen_id}")

    def pop(self, user_id: str) -> Optional[str]:
        if not self._stack[user_id]:
            return None

        self._stack[user_id].pop()

        if not self._stack[user_id]:
            return None

        previous = self._stack[user_id][-1]
        logger.info(f"[STACK] pop → {previous}")
        return previous

    def current(self, user_id: str) -> Optional[str]:
        if not self._stack[user_id]:
            return None
        return self._stack[user_id][-1]

    # =========================
    # MAIN PIPELINE
    # =========================
    async def render(self, screen_id: str, **context: Any) -> ScreenResult:
        user_id = context.get("user_id")

        logger.info(f"[ENGINE] render {screen_id} user={user_id}")

        if user_id:
            self.push(user_id, screen_id)

        # middleware pre
        context = await self.middleware.run_before(screen_id, context)

        # registry render (ALREADY async)
        result: ScreenResult = await self.registry.render(screen_id, **context)

        # middleware post
        result = await self.middleware.run_after(screen_id, context, result)

        # SAFETY GUARD (runtime + mypy alignment)
        if not isinstance(result, dict):
            raise ValueError("ScreenResult must be dict")

        if "text" not in result or "keyboard" not in result:
            raise ValueError("ScreenResult must contain text + keyboard")

        return result