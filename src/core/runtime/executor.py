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

        if cmd.action == "update":
            return self._update(cmd)

        if cmd.action == "add":
            return self._add(cmd)

        if cmd.action == "link":
            return self._link(cmd)

        if cmd.action == "define":
            return self._define(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    # =========================
    # CREATE
    # =========================
    def _create(self, cmd: Command):
        logger.info(f"Creating {cmd.entity_type}: {cmd.name}")

        return {
            "status": "created",
            "entity_type": cmd.entity_type,
            "name": cmd.name
        }

    # =========================
    # UPDATE
    # =========================
    def _update(self, cmd: Command):
        logger.info(
            f"Updating {cmd.entity_type} {cmd.name} "
            f"field={cmd.field} value={cmd.value}"
        )

        return {
            "status": "updated",
            "entity_type": cmd.entity_type,
            "name": cmd.name,
            "field": cmd.field,
            "value": cmd.value
        }

    # =========================
    # ADD (RELATION)
    # =========================
    def _add(self, cmd: Command):
        logger.info(
            f"Adding {cmd.entity_type} {cmd.name} "
            f"to {cmd.target}"
        )

        return {
            "status": "added",
            "relation": "add",
            "entity_type": cmd.entity_type,
            "name": cmd.name,
            "target": cmd.target
        }

    # =========================
    # LINK (GRAPH EDGE)
    # =========================
    def _link(self, cmd: Command):
        logger.info(
            f"Linking {cmd.entity_type} {cmd.name} "
            f"to {cmd.target}"
        )

        return {
            "status": "linked",
            "relation": "link",
            "entity_type": cmd.entity_type,
            "name": cmd.name,
            "target": cmd.target
        }

    # =========================
    # DEFINE (META)
    # =========================
    def _define(self, cmd: Command):
        logger.info(
            f"Defining {cmd.entity_type} {cmd.name} "
            f"{cmd.field}={cmd.value}"
        )

        return {
            "status": "defined",
            "entity_type": cmd.entity_type,
            "name": cmd.name,
            "field": cmd.field,
            "value": cmd.value
        }