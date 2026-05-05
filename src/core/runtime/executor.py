# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (STATE + GRAPH aligned with real API)

from src.core.command.model import Command
from src.core.state.state_manager import StateManager
from src.core.graph.relation_store import RelationStore
from src.core.graph.relation_types import RelationType
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

        if cmd.action in ("add", "link"):
            return self._add_relation(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return None

    # =========================
    # STATE
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
        logger.info(f"Define (alias update) {cmd.name}")
        return self._update(cmd)

    # =========================
    # GRAPH
    # =========================

    def _add_relation(self, cmd: Command):
        target = cmd.target or {}

        from_entity = (cmd.entity_type, cmd.name)
        to_entity = (
            target.get("entity_type"),
            target.get("name")
        )

        # SAFE DEFAULT mapping (no guessing domain logic yet)
        relation = (
            RelationType.HAS_SKILL
            if cmd.action == "add"
            else RelationType.LINK_TO
        )

        logger.info(
            f"[GRAPH] {from_entity} --{relation.name}--> {to_entity}"
        )

        self.graph.add_relation(
            from_entity=from_entity,
            relation=relation,
            to_entity=to_entity
        )

        return {
            "status": "linked",
            "from": from_entity,
            "to": to_entity,
            "relation": relation.name
        }