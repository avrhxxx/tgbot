# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (now with minimal State integration)

from src.core.command.model import Command
from src.core.state.state_manager import StateManager
from src.shared.logging import get_logger

logger = get_logger("Executor")


class Executor:

    def __init__(self):
        self.state = StateManager()

    def execute(self, cmd: Command):
        """
        Executes validated command.
        """

        logger.info(f"Executing command: {cmd}")

        if cmd.action == "create":
            return self._create(cmd)

        if cmd.action == "update":
            return self._update(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    def _create(self, cmd: Command):
        logger.info(f"Creating {cmd.entity_type}: {cmd.name}")

        # STATE WRITE (NEW)
        self.state.create(cmd.entity_type, cmd.name)

        return {
            "status": "created",
            "entity_type": cmd.entity_type,
            "name": cmd.name
        }

    def _update(self, cmd: Command):
        logger.info(f"Updating {cmd.entity_type} {cmd.name} field={cmd.field} value={cmd.value}")

        success = self.state.update(
            cmd.entity_type,
            cmd.name,
            cmd.field,
            cmd.value
        )

        if not success:
            logger.warning("State update failed (entity missing)")
            return {
                "status": "error",
                "reason": "not_found",
                "name": cmd.name
            }

        return {
            "status": "updated",
            "entity_type": cmd.entity_type,
            "name": cmd.name,
            "field": cmd.field,
            "value": cmd.value
        }