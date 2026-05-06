# src/core/runtime/pipeline.py

from src.core.dsl.parser import DSLParser
from src.core.dsl.validator import DSLValidator
from src.core.runtime.executor import Executor
from src.core.state.entity_store import EntityStore
from src.core.graph.relation_store import RelationStore
from src.shared.logging import get_logger

logger = get_logger("pipeline")


class Pipeline:

    def __init__(self):
        self.parser = DSLParser()
        self.validator = DSLValidator()

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