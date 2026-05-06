# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: Main execution pipeline (DSL → parse → validate → execute)

from src.core.dsl.parser import DSLParser
from src.core.dsl.validator import DSLValidator
from src.core.runtime.executor import Executor
from src.shared.logging import get_logger

logger = get_logger("pipeline")


class Pipeline:
    """
    Core deterministic pipeline.
    """

    def __init__(self):
        self.parser = DSLParser()
        self.validator = DSLValidator()
        self.executor = Executor()

    def run(self, text: str):
        logger.info("PIPELINE START")

        # 1. Parse
        ast = self.parser.parse(text)
        logger.info(f"Parsed AST: {ast}")

        # 2. Validate
        self.validator.validate(ast)
        logger.info("Validation passed")

        # 3. Execute
        result = self.executor.execute(ast)
        logger.info("Execution finished")

        return result