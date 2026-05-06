# src/core/dsl/ast.py
# GROUP: core.dsl
# DESCRIPTION: AST (Abstract Syntax Tree) definitions for DSL commands

from dataclasses import dataclass
from typing import List, Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class CommandNode(ASTNode):
    """Represents a single DSL command."""
    name: str
    args: List[Any]