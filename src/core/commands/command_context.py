# src/core/commands/command_context.py
# GROUP: core.commands
# DESCRIPTION: Runtime execution context for command pipeline

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class CommandContext:
    """
    Carries execution metadata through router → executor pipeline.
    """

    user_id: str
    source: str = "telegram"
    trace_id: str = ""

    meta: Dict[str, Any] = field(default_factory=dict)