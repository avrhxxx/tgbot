# src/core/vertex/router.py
# GROUP: core.vertex
# DESCRIPTION: Temporary rule-based router (will be replaced by Vertex AI LLM layer)

from src.core.command.model import Command
from src.shared.logging import get_logger

logger = get_logger("VertexRouter")


class VertexRouter:

    def route(self, text: str) -> Command:
        """
        Converts natural language → Command
        (MVP placeholder before LLM integration)
        """

        logger.info(f"Routing input: {text}")

        # TEMP LOGIC (replace with Vertex AI later)
        if "create hero" in text.lower():
            name = text.split('"')[1] if '"' in text else "unknown"

            return Command(
                action="create",
                entity_type="hero",
                name=name
            )

        return Command(
            action="unknown",
            entity_type="unknown",
            name="unknown"
        )