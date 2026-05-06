# ============================================================
# FILE: src/core/runtime/executor.py
# PURPOSE: Command execution engine
# ============================================================

class Executor:
    def __init__(self, entity_store, relation_store):
        self.entity_store = entity_store
        self.relation_store = relation_store

    def execute(self, command):
        """
        Executes a single AST command
        """

        if command.type == "create_entity":
            self.entity_store.create(command.entity_name, command.entity_type)

        elif command.type == "set_field":
            self.entity_store.set_field(command.entity, command.field, command.value)

        elif command.type == "add_relation":
            self.relation_store.add(command.source, command.relation, command.target)