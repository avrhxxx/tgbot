# src/core/dsl/parser.py
# GROUP: core.dsl
# DESCRIPTION: DSL parser (text → AST). Deterministic, no AI.

from typing import List
from src.core.dsl.ast import CommandNode


class DSLParser:
    """
    Deterministic DSL parser.
    Converts raw text → structured AST (type + params).
    """

    def parse(self, text: str) -> List[CommandNode]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        commands: List[CommandNode] = []

        for line in lines:
            parts = line.split()
            if not parts:
                continue

            op = parts[0].lower()

            # -------------------------------------------------
            # CREATE ENTITY
            # create entity "Tarzan"
            # -------------------------------------------------
            if op == "create" and len(parts) > 2 and parts[1] == "entity":
                name = parts[2].strip('"')

                commands.append(CommandNode(
                    type="create_entity",
                    params={
                        "name": name
                    },
                    raw=line
                ))

            # -------------------------------------------------
            # SET FIELD
            # set field "Tarzan" "hp" "800"
            # -------------------------------------------------
            elif op == "set" and len(parts) > 4 and parts[1] == "field":
                entity = parts[2].strip('"')
                field = parts[3].strip('"')
                value = parts[4].strip('"')

                commands.append(CommandNode(
                    type="set_field",
                    params={
                        "entity": entity,
                        "field": field,
                        "value": value
                    },
                    raw=line
                ))

            # -------------------------------------------------
            # ADD RELATION
            # add relation "Tarzan" "drops" "Iron Sword"
            # -------------------------------------------------
            elif op == "add" and len(parts) > 4 and parts[1] == "relation":
                source = parts[2].strip('"')
                relation = parts[3].strip('"')
                target = parts[4].strip('"')

                commands.append(CommandNode(
                    type="add_relation",
                    params={
                        "from": source,
                        "relation": relation,
                        "to": target
                    },
                    raw=line
                ))

            else:
                raise ValueError(f"Unknown DSL command: {line}")

        return commands