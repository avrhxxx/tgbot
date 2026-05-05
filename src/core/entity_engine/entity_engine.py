# src/core/entity_engine/entity_engine.py
# GROUP: core.entity_engine
# DESCRIPTION: Core Entity Engine (validation + schema enforcement + attr resolution)

import logging
from typing import Any

from src.core.entity_engine.entity_schema import ENTITY_SCHEMAS
from src.core.commands.command_model import Command

logger = logging.getLogger("core.entity_engine")


class EntityEngine:
    """
    CORE GAME WORLD ENGINE

    Responsibilities:
    - Validate commands against schema
    - Resolve entity structure
    - Enforce field rules
    - Normalize updates
    """

    # =========================
    # ENTRY POINT
    # =========================

    def process(self, command: Command) -> Command:
        """
        Takes AST Command → returns validated + normalized Command
        """

        logger.info(
            "🧠 EntityEngine processing | action=%s entity=%s target=%s",
            command.action,
            command.entity,
            command.target,
        )

        schema = self._get_schema(command.entity)

        if not schema:
            raise ValueError(f"No schema found for entity: {command.entity}")

        if command.action == "create":
            return self._validate_create(command, schema)

        if command.action == "update":
            return self._validate_update(command, schema)

        if command.action == "define":
            return self._validate_define(command, schema)

        if command.action == "link":
            return self._validate_link(command, schema)

        return command

    # =========================
    # SCHEMA LOOKUP
    # =========================

    def _get_schema(self, entity_type: str):
        return ENTITY_SCHEMAS.get(entity_type)

    # =========================
    # CREATE VALIDATION
    # =========================

    def _validate_create(self, command: Command, schema: Any) -> Command:
        if command.entity not in ENTITY_SCHEMAS:
            raise ValueError(f"Invalid entity type: {command.entity}")

        logger.info("✔ CREATE validated for %s", command.entity)
        return command

    # =========================
    # UPDATE VALIDATION
    # =========================

    def _validate_update(self, command: Command, schema: Any) -> Command:

        # attr is now canonical (NOT field)
        if not command.attr:
            logger.warning("⚠ update without attr - allowed but unsafe")

        if command.attr and command.attr not in schema.fields:
            raise ValueError(
                f"Attr '{command.attr}' not valid for entity '{command.entity}'"
            )

        # type normalization
        if command.attr:
            field_schema = schema.fields[command.attr]

            command.value = self._normalize_value(
                command.value,
                field_schema.type,
            )

            self._apply_constraints(command, field_schema)

        logger.info("✔ UPDATE validated for %s", command.entity)
        return command

    # =========================
    # DEFINE VALIDATION
    # =========================

    def _validate_define(self, command: Command, schema: Any) -> Command:
        logger.info("✔ DEFINE validated for %s", command.entity)
        return command

    # =========================
    # LINK VALIDATION
    # =========================

    def _validate_link(self, command: Command, schema: Any) -> Command:

        if not command.relation:
            logger.warning("⚠ link without relation payload")

        logger.info("✔ LINK validated for %s", command.entity)
        return command

    # =========================
    # VALUE NORMALIZATION
    # =========================

    def _normalize_value(self, value: Any, expected_type: str):

        if value is None:
            return value

        try:
            if expected_type == "int":
                return int(value)

            if expected_type == "str":
                return str(value)

            if expected_type == "float":
                return float(value)

        except Exception:
            raise ValueError(
                f"Type conversion failed: {value} → {expected_type}"
            ) from None

        return value

    # =========================
    # CONSTRAINTS ENGINE
    # =========================

    def _apply_constraints(self, command: Command, field_schema: Any):

        if field_schema.min_value is not None:
            if command.value < field_schema.min_value:
                raise ValueError(
                    f"Value {command.value} below min {field_schema.min_value}"
                )

        if field_schema.max_value is not None:
            if command.value > field_schema.max_value:
                raise ValueError(
                    f"Value {command.value} above max {field_schema.max_value}"
                )