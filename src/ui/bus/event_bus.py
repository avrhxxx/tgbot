# =========================================
# GROUP: ui.bus
# FILE: event_bus.py
# =========================================

import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on(self, event: str, handler: Callable):
        self._handlers.setdefault(event, []).append(handler)

    async def emit(self, event: str, payload: dict[str, Any]):
        handlers = self._handlers.get(event, [])

        logger.debug("Event emitted: %s", event)

        for h in handlers:
            await h(payload)