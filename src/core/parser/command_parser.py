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

    Supported:
    - create entity
    - update entity field
    - add relation
    - link entities
    - define metadata
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
        # UPDATE
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
        # LINK (GRAPH EDGE)
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
        # DEFINE (META)
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
        # UNKNOWN
        # =========================
        logger.warning("Failed to parse command")

        return Command(
            action="unknown",
            entity_type="unknown",
            name="unknown"
        )