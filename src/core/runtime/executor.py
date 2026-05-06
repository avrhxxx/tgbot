# src/core/runtime/executor.py
# PURPOSE: Command execution engine (resilient DSL AST → Graph operations)

class Executor:

    def __init__(self, entity_store, relation_store):
        self.entity_store = entity_store
        self.relation_store = relation_store

    def execute(self, commands):
        results = []

        for command in commands:

            # -------------------------
            # SKIP INVALID COMMANDS
            # -------------------------
            if hasattr(command, "_valid") and command._valid is False:
                results.append({
                    "status": "error",
                    "type": command.type,
                    "error": command._error
                })
                continue

            try:
                # ---------------------
                # CREATE ENTITY
                # ---------------------
                if command.type == "create_entity":
                    name = command.params["name"]
                    self.entity_store.create_entity(name)

                # ---------------------
                # SET FIELD
                # ---------------------
                elif command.type == "set_field":
                    self.entity_store.set_field(
                        command.params["entity"],
                        command.params["field"],
                        command.params["value"]
                    )

                # ---------------------
                # ADD RELATION
                # ---------------------
                elif command.type == "add_relation":
                    self.relation_store.add_relation(
                        command.params["from"],
                        command.params["relation"],
                        command.params["to"]
                    )

                else:
                    raise ValueError(f"Unknown command type: {command.type}")

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