# src/core/command/model.py
# GROUP: core.command
# DESCRIPTION: Core Command Contract (single source of truth for AI → system execution)

from dataclasses import dataclass
from typing import Any, Optional, Dict


@dataclass
class Command:
    """
    Core execution unit of the system.

    Everything (AI, Telegram, API) MUST resolve into this format.
    """

    action: str              # create / update / link / query
    entity_type: str         # hero / item / skill / building
    name: str                # primary entity name

    field: Optional[str] = None
    value: Any = None
    target: Optional[Dict[str, Any]] = None