# src/core/parser/command_parser.py
# GROUP: core.parser
# DESCRIPTION: Strict DSL parser (text → Command)

import re

from src.core.command.model import Command
from src.shared.logging import get_logger

logger = get_logger("CommandParser")


class CommandParser:
    """
    Parses STRICT DSL commands into Command objects.
    """

    def parse(self, text: str) -> Command:
        logger.info(f"Parsing text: {text}")

        text = text.strip()

        # =========================
        # CREATE
        # =========================
        create_match = re.match(
            r'^create\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if create_match:
            entity_type, name = create_match.groups()

            return Command(
                action="create",
                entity_type=entity_type,
                name=name
            )

        # =========================
        # UPDATE (simple)
        # =========================
        update_match = re.match(
            r'^update\s+(\w+)\s+"([^"]+)"\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if update_match:
            entity_type, name, field, value = update_match.groups()

            return Command(
                action="update",
                entity_type=entity_type,
                name=name,
                field=field,
                value=value
            )

        # =========================
        # UPDATE (nested: update skill X of hero Y field Z)
        # =========================
        nested_update = re.match(
            r'^update\s+(\w+)\s+"([^"]+)"\s+of\s+(\w+)\s+"([^"]+)"\s+field\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if nested_update:
            field, value, parent_type, parent_name, sub_type, sub_name = nested_update.groups()

            return Command(
                action="update",
                entity_type=sub_type,
                name=sub_name,
                field=field,
                value=value,
                target={
                    "entity_type": parent_type,
                    "name": parent_name
                }
            )

        # =========================
        # ADD (RELATION)
        # =========================
        add_match = re.match(
            r'^add\s+(\w+)\s+"([^"]+)"\s+to\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if add_match:
            entity_type, name, target_type, target_name = add_match.groups()

            return Command(
                action="add",
                entity_type=entity_type,
                name=name,
                target={
                    "entity_type": target_type,
                    "name": target_name
                }
            )

        # =========================
        # LINK
        # =========================
        link_match = re.match(
            r'^link\s+(\w+)\s+"([^"]+)"\s+to\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if link_match:
            entity_type, name, target_type, target_name = link_match.groups()

            return Command(
                action="link",
                entity_type=entity_type,
                name=name,
                target={
                    "entity_type": target_type,
                    "name": target_name
                }
            )

        # =========================
        # DEFINE
        # =========================
        define_match = re.match(
            r'^define\s+(\w+)\s+"([^"]+)"\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if define_match:
            entity_type, name, field, value = define_match.groups()

            return Command(
                action="define",
                entity_type=entity_type,
                name=name,
                field=field,
                value=value
            )

        # =========================
        # SHOW
        # =========================
        show_match = re.match(
            r'^show\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if show_match:
            entity_type, name = show_match.groups()

            return Command(
                action="show",
                entity_type=entity_type,
                name=name
            )

        # =========================
        # EXISTS
        # =========================
        exists_match = re.match(
            r'^exists\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if exists_match:
            entity_type, name = exists_match.groups()

            return Command(
                action="exists",
                entity_type=entity_type,
                name=name
            )

        # =========================
        # SCHEMA
        # =========================
        schema_match = re.match(
            r'^schema\s+(\w+)$',
            text,
            re.IGNORECASE
        )

        if schema_match:
            entity_type = schema_match.group(1)

            return Command(
                action="schema",
                entity_type=entity_type,
                name="*"
            )

        # =========================
        # MISSING FIELDS
        # =========================
        missing_match = re.match(
            r'^missing_fields\s+(\w+)\s+"([^"]+)"$',
            text,
            re.IGNORECASE
        )

        if missing_match:
            entity_type, name = missing_match.groups()

            return Command(
                action="missing_fields",
                entity_type=entity_type,
                name=name
            )

        # =========================
        # UNKNOWN
        # =========================
        logger.warning("Failed to parse command")

        return Command(
            action="unknown",
            entity_type="unknown",
            name="unknown"
        )