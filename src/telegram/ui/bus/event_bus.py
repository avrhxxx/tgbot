# =========================================
# GROUP: telegram.ui.bus
# FILE: event_bus.py
# =========================================

import logging
from collections import defaultdict
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)


class EventBus:
    """
    Lightweight UI event bus.
    Only routes UI events -> controller.
    """

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def on(self, event: str, handler: Callable):
        self._handlers[event].append(handler)

    async def emit(self, event: str, **data):
        logger.info("UI Event emitted | event=%s", event)

        for handler in self._handlers.get(event, []):
            await handler(**data)


event_bus = EventBus()