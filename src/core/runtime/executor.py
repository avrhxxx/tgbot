# src/core/runtime/executor.py
# PURPOSE: Command execution engine

class Executor:
    def __init__(self, entity_store, relation_store):
        self.entity_store = entity_store
        self.relation_store = relation_store

    def execute(self, commands):
        """
        Executes list of AST commands
        """

        results = []

        for command in commands:

            # CREATE ENTITY
            if command.name == "create":
                # create entity "Tarzan"
                entity_name = command.args[1]
                self.entity_store.create_entity(entity_name)

            # SET FIELD
            elif command.name == "set":
                # set field "Tarzan" "hp" "800"
                entity = command.args[1]
                field = command.args[2]
                value = command.args[3]

                self.entity_store.set_field(entity, field, value)

            # ADD RELATION
            elif command.name == "add":
                # add relation "Tarzan" "has_skill" "Skill"
                source = command.args[1]
                relation = command.args[2]
                target = command.args[3]

                self.relation_store.add_relation(source, relation, target)

            results.append({"status": "ok", "command": command.name})

        return results