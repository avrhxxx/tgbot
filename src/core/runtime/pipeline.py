# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: DSL execution pipeline (Stage 1 compiler runtime)

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
    """
    Stage 1 Execution Pipeline

    FLOW:
    DSL TEXT → PARSE → VALIDATE → EXECUTE → RESULT
    """

    def __init__(self):

        # -----------------------------
        # DSL CORE
        # -----------------------------
        self.parser = DSLParser()

        # -----------------------------
        # REGISTRIES (Stage 1 in-memory)
        # -----------------------------
        self.type_registry = TypeRegistry()
        self.field_registry = FieldRegistry()
        self.relation_registry = RelationRegistry()

        self.validator = DSLValidator(
            type_registry=self.type_registry,
            field_registry=self.field_registry,
            relation_registry=self.relation_registry
        )

        # -----------------------------
        # GRAPH STATE (IN-MEMORY)
        # -----------------------------
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

        # 1. PARSE
        ast = self.parser.parse(text)
        logger.info(f"Parsed AST: {ast}")

        # 2. VALIDATE (non-destructive)
        validated_ast = self.validator.validate(ast)
        logger.info("Validation passed")

        # 3. EXECUTE
        result = self.executor.execute(validated_ast)

        logger.info("Execution finished")

        return result