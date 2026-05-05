# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (future: Firestore / Sheets / DB integration)

from src.core.command.model import Command
from src.shared.logging import get_logger

logger = get_logger("Executor")


class Executor:

    def execute(self, cmd: Command):
        """
        Executes validated command.
        This is where Firestore / Sheets / game world updates will happen.
        """

        logger.info(f"Executing command: {cmd}")

        if cmd.action == "create":
            return self._create(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    def _create(self, cmd: Command):
        logger.info(f"Creating {cmd.entity_type}: {cmd.name}")

        # placeholder for DB write
        return {
            "status": "created",
            "entity_type": cmd.entity_type,
            "name": cmd.name
        }