from typing import List
import re

from src.core.dsl.ast import CommandNode


class DSLParser:

    STRING_RE = re.compile(r'"([^"]*)"')

    def parse(self, text: str) -> List[CommandNode]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        commands: List[CommandNode] = []

        for line in lines:
            lower = line.lower()
            quoted = self.STRING_RE.findall(line)

            # -----------------------------
            # CREATE ENTITY
            # -----------------------------
            if lower.startswith("create entity"):
                commands.append(CommandNode(
                    type="create_entity",
                    params={"name": quoted[0]},
                    raw=line
                ))

            # -----------------------------
            # CREATE TYPE
            # create type "hero"
            # -----------------------------
            elif lower.startswith("create type"):
                commands.append(CommandNode(
                    type="create_type",
                    params={"name": quoted[0]},
                    raw=line
                ))

            # -----------------------------
            # CREATE FIELD
            # create field "hp"
            # -----------------------------
            elif lower.startswith("create field"):
                commands.append(CommandNode(
                    type="create_field",
                    params={"name": quoted[0]},
                    raw=line
                ))

            # -----------------------------
            # CREATE RELATION
            # create relation "drops"
            # -----------------------------
            elif lower.startswith("create relation"):
                commands.append(CommandNode(
                    type="create_relation",
                    params={"name": quoted[0]},
                    raw=line
                ))

            # -----------------------------
            # SET ENTITY TYPE
            # set entity type "Tarzan" "hero"
            # -----------------------------
            elif lower.startswith("set entity type"):
                commands.append(CommandNode(
                    type="set_entity_type",
                    params={
                        "entity": quoted[0],
                        "type": quoted[1]
                    },
                    raw=line
                ))

            # -----------------------------
            # SET FIELD
            # -----------------------------
            elif lower.startswith("set field"):
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
            # -----------------------------
            elif lower.startswith("add relation"):
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