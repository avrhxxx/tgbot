# src/core/runtime/executor.py
# GROUP: core.runtime
# DESCRIPTION: Execution layer (STATE + GRAPH CI-safe version + DSL v2 queries)

from src.core.command.model import Command
from src.core.state.state_manager import StateManager
from src.core.graph.relation_store import RelationStore
from src.core.graph.relation_types import (
    HAS_SKILL,
    LINK_TO_FACTION,
    GENERIC_LINK,
)
from src.shared.logging import get_logger

logger = get_logger("Executor")


class Executor:

    def __init__(self):
        self.state = StateManager()
        self.graph = RelationStore()

    def execute(self, cmd: Command):
        logger.info(f"Executing command: {cmd}")

        # =========================
        # STATE
        # =========================
        if cmd.action == "create":
            return self._create(cmd)

        if cmd.action == "update":
            return self._update(cmd)

        if cmd.action == "define":
            return self._define(cmd)

        # =========================
        # GRAPH
        # =========================
        if cmd.action in ("add", "link"):
            return self._add_relation(cmd)

        # =========================
        # QUERY LAYER (DSL v2)
        # =========================
        if cmd.action == "show":
            return self._show(cmd)

        if cmd.action == "exists":
            return self._exists(cmd)

        if cmd.action == "schema":
            return self._schema(cmd)

        if cmd.action == "missing_fields":
            return self._missing_fields(cmd)

        logger.warning(f"Unknown action: {cmd.action}")
        return {"status": "error", "reason": "unknown_action"}

    # =========================
    # STATE
    # =========================

    def _create(self, cmd: Command):
        self.state.create(cmd.entity_type, cmd.name)

        return {
            "status": "created",
            "entity_type": cmd.entity_type,
            "name": cmd.name
        }

    def _update(self, cmd: Command):
        if not cmd.field or cmd.value is None:
            return {"status": "error"}

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
        return self._update(cmd)

    # =========================
    # GRAPH
    # =========================

    def _resolve_relation(self, cmd: Command):

        if cmd.action == "add":
            if cmd.entity_type == "skill":
                return HAS_SKILL
            return GENERIC_LINK

        if cmd.action == "link":
            return LINK_TO_FACTION

        return GENERIC_LINK

    def _add_relation(self, cmd: Command):
        target = cmd.target or {}

        from_entity = (cmd.entity_type, cmd.name)

        to_type = target.get("entity_type") or "unknown"
        to_name = target.get("name") or "unknown"

        to_entity = (to_type, to_name)

        relation = self._resolve_relation(cmd)

        logger.info(
            f"[GRAPH] {from_entity} --{relation}--> {to_entity}"
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
            "relation": relation
        }

    # =========================
    # QUERY LAYER (MVP STUBS)
    # =========================

    def _show(self, cmd: Command):
        data = self.state.get(cmd.entity_type, cmd.name)
        return {
            "status": "ok",
            "entity": cmd.name,
            "data": data
        }

    def _exists(self, cmd: Command):
        exists = self.state.exists(cmd.entity_type, cmd.name)
        return {
            "status": "ok",
            "exists": exists,
            "entity": cmd.name
        }

    def _schema(self, cmd: Command):
        return {
            "status": "ok",
            "entity_type": cmd.entity_type,
            "schema": self.state.schema(cmd.entity_type)
        }

    def _missing_fields(self, cmd: Command):
        missing = self.state.missing_fields(cmd.entity_type, cmd.name)

        return {
            "status": "ok",
            "entity": cmd.name,
            "missing_fields": missing
        }