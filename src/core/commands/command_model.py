# src/core/commands/command_model.py
# GROUP: core.commands
# DESCRIPTION: Core AST model for DSL command system (single source of truth)

from dataclasses import dataclass, field
from typing import Any, Optional, Dict


@dataclass
class Command:
    """
    Unified AST node for all AI/admin DSL operations.
    This is the ONLY structure that downstream systems understand.
    """

    action: str                 # create | update | link | define | show | exists | add | missing_fields | schema
    entity: str                 # hero | skill | item | building | research_tree | research_node
    target: Optional[str] = None  # name of entity (e.g. "Tarzan")
    field: Optional[str] = None   # field name (e.g. "damage", "tier")
    value: Any = None             # value for update/define
    relation: Optional[Dict[str, Any]] = None  # links (hero -> faction etc.)
    context: Dict[str, Any] = field(default_factory=dict)

    def is_create(self) -> bool:
        return self.action == "create"

    def is_update(self) -> bool:
        return self.action == "update"

    def is_link(self) -> bool:
        return self.action == "link"