# src/core/runtime/pipeline.py

from src.core.dsl.parser import DSLParser
from src.core.dsl.validator import DSLValidator
from src.core.runtime.executor import Executor

from src.core.state.entity_store import EntityStore
from src.core.graph.relation_store import RelationStore

from src.domain.types.type_registry import TypeRegistry
from src.domain.fields.field_registry import FieldRegistry
from src.domain.relations.relation_registry import RelationRegistry

from src.shared.logging import get_logger

logger = get_logger("pipeline")


class Pipeline:

    def __init__(self):

        # DSL CORE
        self.parser = DSLParser()

        # REGISTRY LAYER (IN-MEMORY STAGE 1)
        self.type_registry = TypeRegistry()
        self.field_registry = FieldRegistry()
        self.relation_registry = RelationRegistry()

        self.validator = DSLValidator(
            type_registry=self.type_registry,
            field_registry=self.field_registry,
            relation_registry=self.relation_registry
        )

        # GRAPH STATE (IN-MEMORY STAGE 1)
        self.entity_store = EntityStore()
        self.relation_store = RelationStore()

        self.executor = Executor(
            entity_store=self.entity_store,
            relation_store=self.relation_store
        )

    def handle(self, text: str):
        return self.run(text)

    def run(self, text: str):
        logger.info("PIPELINE START")

        ast = self.parser.parse(text)
        logger.info(f"Parsed AST: {ast}")

        self.validator.validate(ast)
        logger.info("Validation passed")

        result = self.executor.execute(ast)
        logger.info("Execution finished")

        return result