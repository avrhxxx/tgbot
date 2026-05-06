# src/core/dsl/parser.py
# GROUP: core.dsl
# DESCRIPTION: DSL Parser (Stage 1 - safe deterministic AST builder)

from typing import List, Optional
import re

from src.core.dsl.ast import CommandNode


class DSLParser:

    STRING_RE = re.compile(r'"([^"]*)"')

    def _safe_get(self, arr: List[str], index: int) -> Optional[str]:
        if index < len(arr):
            return arr[index]
        return None

    def parse(self, text: str) -> List[CommandNode]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        commands: List[CommandNode] = []

        for line in lines:
            lower = line.lower()
            quoted = self.STRING_RE.findall(line)

            try:

                # -----------------------------
                # CREATE ENTITY
                # -----------------------------
                if lower.startswith("create entity") and len(quoted) >= 1:
                    commands.append(CommandNode(
                        type="create_entity",
                        params={"name": quoted[0]},
                        raw=line
                    ))

                # -----------------------------
                # CREATE TYPE
                # -----------------------------
                elif lower.startswith("create type") and len(quoted) >= 1:
                    commands.append(CommandNode(
                        type="create_type",
                        params={"name": quoted[0]},
                        raw=line
                    ))

                # -----------------------------
                # CREATE FIELD
                # -----------------------------
                elif lower.startswith("create field") and len(quoted) >= 1:
                    commands.append(CommandNode(
                        type="create_field",
                        params={"name": quoted[0]},
                        raw=line
                    ))

                # -----------------------------
                # CREATE RELATION
                # -----------------------------
                elif lower.startswith("create relation") and len(quoted) >= 1:
                    commands.append(CommandNode(
                        type="create_relation",
                        params={"name": quoted[0]},
                        raw=line
                    ))

                # -----------------------------
                # SET ENTITY TYPE
                # -----------------------------
                elif lower.startswith("set entity type") and len(quoted) >= 2:
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
                elif lower.startswith("set field") and len(quoted) >= 3:
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
                elif lower.startswith("add relation") and len(quoted) >= 3:
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
                    # FAIL SAFE (NO CRASH)
                    commands.append(CommandNode(
                        type="invalid_command",
                        params={"error": f"Invalid DSL: {line}"},
                        raw=line
                    ))

            except Exception as e:
                # HARD SAFETY NET (Stage 1 requirement)
                commands.append(CommandNode(
                    type="invalid_command",
                    params={"error": str(e)},
                    raw=line
                ))

        return commands