# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (now with minimal State integration + safe typing)

from typing import Any

from src.core.command.model import Command
from src.core.state.state_manager import StateManager
from src.shared.logging import get_logger

logger = get_logger("Executor")


class Executor:

    def __init__(self):
        self.state = StateManager()

    def execute(self, cmd: Command):
        logger.info(f"Executing command: {cmd}")

        if cmd.action == "create":
            return self._create(cmd)

        if cmd.action == "update":
            return self._update(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    def _create(self, cmd: Command):
        logger.info(f"Creating {cmd.entity_type}: {cmd.name}")

        self.state.create(cmd.entity_type, cmd.name)

        return {
            "status": "created",
            "entity_type": cmd.entity_type,
            "name": cmd.name
        }

    def _update(self, cmd: Command):
        if not cmd.field:
            logger.warning("Missing field in update command")
            return {
                "status": "error",
                "reason": "missing_field",
                "name": cmd.name
            }

        if cmd.value is None:
            logger.warning("Missing value in update command")
            return {
                "status": "error",
                "reason": "missing_value",
                "name": cmd.name,
                "field": cmd.field
            }

        field: str = str(cmd.field)
        value: Any = cmd.value

        logger.info(
            f"Updating {cmd.entity_type} {cmd.name} field={field} value={value}"
        )

        success = self.state.update(
            cmd.entity_type,
            cmd.name,
            field,
            value
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
            "field": field,
            "value": value
        }