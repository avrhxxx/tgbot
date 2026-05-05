# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: Full system execution pipeline (Router → Validator → Executor)

from src.core.vertex.router import VertexRouter
from src.core.runtime.executor import Executor
from src.core.command.validator import CommandValidator
from src.shared.logging import get_logger

logger = get_logger("Pipeline")


class Pipeline:

    def __init__(self):
        self.router = VertexRouter()
        self.validator = CommandValidator()
        self.executor = Executor()

    def handle(self, text: str):
        """
        Main entry point of CORE system.
        """

        logger.info(f"Incoming text: {text}")

        cmd = self.router.route(text)

        if not self.validator.validate(cmd):
            logger.warning("Invalid command")
            return "INVALID COMMAND"

        return self.executor.execute(cmd)