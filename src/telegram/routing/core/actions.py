# =========================================
# GROUP: telegram.routing.core
# FILE: actions.py
# DESCRIPTION:
# Core routing action model for routing v2 system.
# Defines typed navigation contracts for UI layer.
# =========================================

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class RouteAction:
    """
    Core navigation unit used across entire bot UI.
    Replaces string-based routing identifiers.
    """
    id: str
    target: str
    handler: Callable[..., Any] | None = None