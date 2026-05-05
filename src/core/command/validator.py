# src/core/command/validator.py
# GROUP: core.command
# DESCRIPTION: Validates Command integrity before execution

from src.core.command.model import Command
from src.shared.logging import get_logger

logger = get_logger("CommandValidator")


class CommandValidator:

    def validate(self, cmd: Command) -> bool:
        """
        Ensures command is structurally valid before execution layer.
        """

        if not cmd.action:
            logger.warning("Missing action")
            return False

        if not cmd.entity_type:
            logger.warning("Missing entity_type")
            return False

        if not cmd.name:
            logger.warning("Missing name")
            return False

        return True