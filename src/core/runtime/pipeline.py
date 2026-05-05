# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: Full system execution pipeline (Parser → Router fallback → Validator → Executor)

from src.core.vertex.router import VertexRouter
from src.core.runtime.executor import Executor
from src.core.command.validator import CommandValidator
from src.core.parser.command_parser import CommandParser
from src.shared.logging import get_logger

logger = get_logger("Pipeline")


class Pipeline:

    def __init__(self):
        self.router = VertexRouter()
        self.parser = CommandParser()  # 🔥 NEW
        self.validator = CommandValidator()
        self.executor = Executor()

    def handle(self, text: str):
        """
        Main entry point of CORE system.
        """

        logger.info(f"Incoming text: {text}")

        # =========================
        # STEP 1: TRY DSL PARSER
        # =========================
        cmd = self.parser.parse(text)

        if cmd.action != "unknown":
            logger.info("Command parsed via DSL parser")

        else:
            # =========================
            # STEP 2: FALLBACK ROUTER
            # =========================
            logger.info("Falling back to router")
            cmd = self.router.route(text)

        # =========================
        # STEP 3: VALIDATION
        # =========================
        if not self.validator.validate(cmd):
            logger.warning("Invalid command")
            return "INVALID COMMAND"

        # =========================
        # STEP 4: EXECUTION
        # =========================
        return self.executor.execute(cmd)