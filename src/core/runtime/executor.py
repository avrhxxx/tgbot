# src/core/runtime/executor.py
# PURPOSE: Command execution engine (Stage 1 FULL SAFE DISPATCH)

from src.shared.logging import get_logger

logger = get_logger("executor")


class Executor:

    def __init__(self, entity_store):
        self.entity_store = entity_store

    def execute(self, commands):
        results = []

        for command in commands:

            if hasattr(command, "_valid") and command._valid is False:
                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": command._error
                })
                continue

            try:

                # =========================
                # ENTITY
                # =========================
                if command.type == "create_entity":
                    self.entity_store.create_entity(
                        command.params["name"]
                    )

                # =========================
                # FIELD
                # =========================
                elif command.type == "set_field":
                    self.entity_store.set_field(
                        command.params["entity"],
                        command.params["field"],
                        command.params["value"]
                    )

                # =========================
                # RELATION (NOW INSIDE ENTITY STORE)
                # =========================
                elif command.type == "add_relation":
                    self.entity_store.add_relation(
                        command.params["from"],
                        command.params["relation"],
                        command.params["to"]
                    )

                # =========================
                # STAGE 1 BOOTSTRAP OPS (NO-OP SAFE)
                # =========================

                elif command.type == "create_type":
                    pass

                elif command.type == "create_field":
                    pass

                elif command.type == "create_relation":
                    pass

                elif command.type == "set_entity_type":
                    self.entity_store.set_entity_type(
                        command.params["entity"],
                        command.params["type"]
                    )

                else:
                    results.append({
                        "status": "error",
                        "type": command.type,
                        "error": f"Unsupported command (executor): {command.type}"
                    })
                    continue

                results.append({
                    "status": "ok",
                    "type": command.type
                })

            except Exception as e:
                logger.exception("Executor crash")
                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": str(e)
                })

        return results