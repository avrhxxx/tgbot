# src/core/runtime/executor.py
# PURPOSE: Command execution engine (Stage 1 FULL SAFE DISPATCH - FINAL)

from src.shared.logging import get_logger

logger = get_logger("executor")


class Executor:
    """
    Deterministic command executor.

    RULES:
    - NEVER throws exceptions outside
    - NEVER blocks pipeline
    - ALWAYS returns structured result
    - Errors are events, not failures
    """

    def __init__(self, entity_store):
        self.entity_store = entity_store

    def execute(self, commands):
        results = []

        for command in commands:

            # =========================
            # PRE-VALIDATION FLAG
            # =========================
            if hasattr(command, "_valid") and command._valid is False:
                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": command._error,
                    "stage": "validation"
                })
                continue

            try:

                # =========================
                # ENTITY OPS
                # =========================
                if command.type == "create_entity":
                    self.entity_store.create_entity(
                        command.params["name"]
                    )

                # =========================
                # FIELD OPS
                # =========================
                elif command.type == "set_field":
                    self.entity_store.set_field(
                        command.params["entity"],
                        command.params["field"],
                        command.params["value"]
                    )

                # =========================
                # RELATION OPS (delegated to entity_store)
                # =========================
                elif command.type == "add_relation":
                    self.entity_store.add_relation(
                        command.params["from"],
                        command.params["relation"],
                        command.params["to"]
                    )

                # =========================
                # TYPE SYSTEM (BOOTSTRAP SAFE)
                # =========================
                elif command.type == "create_type":
                    pass  # Stage 1: registry only, no runtime effect

                elif command.type == "create_field":
                    pass  # Stage 1: registry only

                elif command.type == "create_relation":
                    pass  # Stage 1: registry only

                # =========================
                # ENTITY TYPE ASSIGNMENT
                # =========================
                elif command.type == "set_entity_type":
                    self.entity_store.set_entity_type(
                        command.params["entity"],
                        command.params["type"]
                    )

                # =========================
                # UNKNOWN COMMAND
                # =========================
                else:
                    results.append({
                        "status": "error",
                        "type": command.type,
                        "error": f"UNKNOWN_COMMAND: {command.type}",
                        "stage": "executor"
                    })
                    continue

                # =========================
                # SUCCESS CASE
                # =========================
                results.append({
                    "status": "ok",
                    "type": command.type
                })

            except Exception as e:
                # =========================
                # HARD SAFETY NET (NEVER CRASH)
                # =========================
                logger.exception(f"Executor safe-catch: {command.type}")

                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": str(e),
                    "stage": "runtime"
                })

        return results