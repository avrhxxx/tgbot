# src/core/commands/command_router.py
# GROUP: core.commands
# DESCRIPTION: Routes AST commands to IndexService (execution layer v1)

import logging
from src.core.commands.command_model import Command

logger = logging.getLogger("core.commands.router")


class CommandRouter:
    """
    Simple execution router (v1).

    Responsibility:
    - Accept Command (AST)
    - Delegate execution to IndexService
    """

    def __init__(self, index_service):
        self.index_service = index_service

    def route(self, command: Command):
        logger.info(
            "📦 Routing command | action=%s entity=%s target=%s",
            command.action,
            command.entity,
            command.target
        )

        # =========================
        # CREATE
        # =========================
        if command.action == "create":
            return self.index_service.create(command)

        # =========================
        # UPDATE
        # =========================
        if command.action == "update":
            return self.index_service.update(command)

        # =========================
        # LINK
        # =========================
        if command.action == "link":
            return self.index_service.link_command(command)

        # =========================
        # DEFINE
        # =========================
        if command.action == "define":
            return self.index_service.define(command)

        # =========================
        # QUERY
        # =========================
        if command.action in ("show", "exists", "missing_fields", "schema"):
            return self.index_service.query(command)

        raise ValueError(f"Unknown command action: {command.action}")