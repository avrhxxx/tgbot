# src/core/dsl/ast.py
# GROUP: core.dsl
# DESCRIPTION: AST (Abstract Syntax Tree) definitions for DSL commands

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ASTNode:
    """
    Base AST node.
    Contains optional raw input for trace/debug purposes.
    """
    raw: Optional[str] = None


@dataclass
class CommandNode(ASTNode):
    """
    Represents a single DSL command in deterministic form.
    """

    type: str
    params: Dict[str, Any]