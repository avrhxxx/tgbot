# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (now unified STATE + GRAPH routing)

from typing import Any

from src.core.command.model import Command
from src.core.state.state_manager import StateManager
from src.core.graph.relation_store import RelationStore
from src.shared.logging import get_logger

logger = get_logger("Executor")


class Executor:

    def __init__(self):
        self.state = StateManager()
        self.graph = RelationStore()

    def execute(self, cmd: Command):
        logger.info(f"Executing command: {cmd}")

        if cmd.action == "create":
            return self._create(cmd)

        if cmd.action == "update":
            return self._update(cmd)

        if cmd.action == "define":
            return self._define(cmd)

        if cmd.action == "add":
            return self._add_relation(cmd)

        if cmd.action == "link":
            return self._add_relation(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    # =========================
    # STATE OPERATIONS
    # =========================

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
            return {"status": "error", "reason": "missing_field"}

        if cmd.value is None:
            return {"status": "error", "reason": "missing_value"}

        logger.info(
            f"Updating {cmd.entity_type} {cmd.name} {cmd.field}={cmd.value}"
        )

        ok = self.state.update(
            cmd.entity_type,
            cmd.name,
            str(cmd.field),
            cmd.value
        )

        return {
            "status": "updated" if ok else "error",
            "name": cmd.name,
            "field": cmd.field,
            "value": cmd.value
        }

    def _define(self, cmd: Command):
        """
        Define = semantic sugar for field update
        """
        logger.info(f"Defining {cmd.entity_type}:{cmd.name} {cmd.field}={cmd.value}")

        return self._update(cmd)

    # =========================
    # GRAPH OPERATIONS
    # =========================

    def _add_relation(self, cmd: Command):
        """
        add/link → graph relation
        """

        target = cmd.target or {}

        logger.info(
            f"Adding relation: {cmd.entity_type}:{cmd.name} -> {target}"
        )

        self.graph.add(
            from_type=cmd.entity_type,
            from_name=cmd.name,
            to_type=target.get("entity_type"),
            to_name=target.get("name"),
            relation=cmd.action
        )

        return {
            "status": "linked",
            "from": {
                "type": cmd.entity_type,
                "name": cmd.name
            },
            "to": target
        }