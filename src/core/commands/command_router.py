# src/core/commands/command_router.py
# GROUP: core.commands
# DESCRIPTION: Routes AST commands to proper service layer

import logging
from src.core.commands.command_model import Command

logger = logging.getLogger("core.commands.router")


class CommandRouter:

    def __init__(self, executor):
        self.executor = executor

    def route(self, command: Command):
        """
        Converts AST → execution pipeline decision
        """

        logger.info(
            "📦 Routing command | action=%s entity=%s target=%s",
            command.action,
            command.entity,
            command.target
        )

        # CREATE FLOW
        if command.action == "create":
            return self.executor.create(command)

        # UPDATE FLOW
        if command.action == "update":
            return self.executor.update(command)

        # LINK FLOW
        if command.action == "link":
            return self.executor.link(command)

        # DEFINE FLOW
        if command.action == "define":
            return self.executor.define(command)

        # QUERY FLOWS
        if command.action in ("show", "exists", "missing_fields", "schema"):
            return self.executor.query(command)

        raise ValueError(f"Unknown command action: {command.action}")