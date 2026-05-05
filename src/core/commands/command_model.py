# src/core/commands/command_model.py
# GROUP: core.commands
# DESCRIPTION: Core AST model for DSL command system (single source of truth)

from dataclasses import dataclass, field as dc_field
from typing import Any, Optional, Dict


@dataclass
class Command:
    """
    Unified AST node for all AI/admin DSL operations.
    This is the ONLY structure that downstream systems understand.
    """

    action: str
    entity: str

    # primary identifier (e.g. "Tarzan")
    target: Optional[str] = None

    # unified field name (IMPORTANT: replaces legacy "field")
    field: Optional[str] = None

    value: Any = None

    relation: Optional[Dict[str, Any]] = None

    context: Dict[str, Any] = dc_field(default_factory=dict)

    # =========================
    # helpers
    # =========================

    def is_create(self) -> bool:
        return self.action == "create"

    def is_update(self) -> bool:
        return self.action == "update"

    def is_link(self) -> bool:
        return self.action == "link"

    def is_define(self) -> bool:
        return self.action == "define"

    def is_query(self) -> bool:
        return self.action in ("show", "exists", "missing_fields", "schema")