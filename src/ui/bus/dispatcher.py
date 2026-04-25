# =========================================
# GROUP: ui.bus
# FILE: dispatcher.py
# DESCRIPTION:
# Simple in-memory event bus (sync for now)
# =========================================

from typing import Callable, Dict, Type, Any


class EventBus:
    def __init__(self):
        self._handlers: Dict[Type, list[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

    def emit(self, event: Any):
        for handler in self._handlers.get(type(event), []):
            handler(event)


bus = EventBus()