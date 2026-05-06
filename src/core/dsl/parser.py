# src/core/dsl/parser.py
# GROUP: core.dsl
# DESCRIPTION: DSL parser (text → AST). Deterministic, no AI.

from typing import List
from src.core.dsl.ast import CommandNode


class DSLParser:
    """
    Minimal deterministic parser.
    NOTE: Placeholder implementation — will be expanded.
    """

    def parse(self, text: str) -> List[CommandNode]:
        """
        Parses raw DSL text into AST nodes.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        commands: List[CommandNode] = []

        for line in lines:
            parts = line.split()
            name = parts[0]
            args = parts[1:]
            commands.append(CommandNode(name=name, args=args))

        return commands