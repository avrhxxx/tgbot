# src/core/runtime/executor.py
# PURPOSE: Command execution engine (Stage 1 FULL SAFE DISPATCH)

class Executor:

    def __init__(self, entity_store, relation_store):
        self.entity_store = entity_store
        self.relation_store = relation_store

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
                    self.entity_store.create_entity(command.params["name"])

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
                # RELATION
                # =========================
                elif command.type == "add_relation":
                    self.relation_store.add_relation(
                        command.params["from"],
                        command.params["relation"],
                        command.params["to"]
                    )

                # =========================
                # STAGE 1 BOOTSTRAP OPS (NO-OP SAFE)
                # =========================

                elif command.type == "create_type":
                    # registry handled elsewhere in Stage 1 future phase
                    pass

                elif command.type == "create_field":
                    # registry placeholder (no-op Stage 1)
                    pass

                elif command.type == "create_relation":
                    # registry placeholder (no-op Stage 1)
                    pass

                elif command.type == "set_entity_type":
                    # entity type assignment not enforced yet in runtime
                    pass

                else:
                    # IMPORTANT: NO CRASH IN STAGE 1
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
                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": str(e)
                })

        return results