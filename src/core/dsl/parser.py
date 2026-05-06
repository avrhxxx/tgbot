# src/core/dsl/parser.py
# GROUP: core.dsl
# DESCRIPTION: DSL parser (text → AST). Deterministic, no AI.

from typing import List
import re

from src.core.dsl.ast import CommandNode


class DSLParser:
    """
    Deterministic DSL parser.
    Converts raw text → structured AST (type + params).
    """

    STRING_RE = re.compile(r'"([^"]*)"')

    def parse(self, text: str) -> List[CommandNode]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        commands: List[CommandNode] = []

        for line in lines:
            lower = line.lower()

            # extract quoted strings safely
            quoted = self.STRING_RE.findall(line)

            # -----------------------------
            # CREATE ENTITY
            # create entity "Tarzan"
            # -----------------------------
            if lower.startswith("create entity"):
                if len(quoted) < 1:
                    raise ValueError(f"Invalid create entity syntax: {line}")

                commands.append(CommandNode(
                    type="create_entity",
                    params={"name": quoted[0]},
                    raw=line
                ))

            # -----------------------------
            # SET FIELD
            # set field "Tarzan" "hp" "800"
            # -----------------------------
            elif lower.startswith("set field"):
                if len(quoted) < 3:
                    raise ValueError(f"Invalid set field syntax: {line}")

                commands.append(CommandNode(
                    type="set_field",
                    params={
                        "entity": quoted[0],
                        "field": quoted[1],
                        "value": quoted[2]
                    },
                    raw=line
                ))

            # -----------------------------
            # ADD RELATION
            # add relation "Tarzan" "drops" "Sword"
            # -----------------------------
            elif lower.startswith("add relation"):
                if len(quoted) < 3:
                    raise ValueError(f"Invalid add relation syntax: {line}")

                commands.append(CommandNode(
                    type="add_relation",
                    params={
                        "from": quoted[0],
                        "relation": quoted[1],
                        "to": quoted[2]
                    },
                    raw=line
                ))

            else:
                raise ValueError(f"Unknown DSL command: {line}")

        return commands