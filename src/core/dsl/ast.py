# src/core/dsl/ast.py
# GROUP: core.dsl
# DESCRIPTION: AST (Abstract Syntax Tree) definitions for DSL commands

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ASTNode:
    """
    Base AST node.
    """
    pass


@dataclass
class CommandNode(ASTNode):
    """
    Represents a single DSL command in deterministic form.
    """

    type: str
    params: Dict[str, Any]
    raw: Optional[str] = None