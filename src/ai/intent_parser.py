# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: STRICT DSL Intent Parser v2 → STABLE AST compiler (Command output)

import logging
import re
from typing import Any, Optional

from src.ai.gemini import GeminiClient
from src.core.commands.command_model import Command

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    ALLOWED_ACTIONS = {
        "create",
        "update",
        "define",
        "add",
        "link",
        "show",
        "exists",
        "missing_fields",
        "schema",
    }

    RELATION_KEYWORDS = {"of", "to", "to_hero", "to_tree", "to_building"}

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser v2 (STABLE AST MODE) initialized")

    # =========================
    # UTIL
    # =========================

    def _extract_quoted(self, text: str):
        return re.findall(r'"([^"]+)"', text)

    def _tokenize(self, text: str):
        quoted = self._extract_quoted(text)
        temp = re.sub(r'"[^"]+"', " __Q__ ", text)
        tokens = temp.split()

        result = []
        q_index = 0

        for t in tokens:
            if t == "__Q__":
                result.append(quoted[q_index])
                q_index += 1
            else:
                result.append(t)

        return result

    # =========================
    # AST COMPILER
    # =========================

    def _to_command(self, tokens: list[str]) -> Command:

        if not tokens:
            raise ValueError("Empty DSL input")

        action = tokens[0]

        if action not in self.ALLOWED_ACTIONS:
            raise ValueError(f"Invalid action: {action}")

        entity: Optional[str] = None
        target: Optional[str] = None
        field: Optional[str] = None
        value: Any = None
        relation: Optional[dict] = None

        # =========================
        # CREATE / DEFINE / ADD
        # =========================
        if action in {"create", "define", "add"}:
            entity = tokens[1] if len(tokens) > 1 else None
            target = tokens[2] if len(tokens) > 2 else None

            # field/value (optional)
            if "field" in tokens:
                i = tokens.index("field")
                if i + 2 < len(tokens):
                    field = tokens[i + 1]
                    value = tokens[i + 2]

            # relation parsing (stable graph edge format)
            for i, t in enumerate(tokens):
                if t in self.RELATION_KEYWORDS and i + 2 < len(tokens):
                    relation = {
                        "relation": t,
                        "target_type": tokens[i + 1],
                        "target": tokens[i + 2],
                    }

        # =========================
        # UPDATE
        # =========================
        elif action == "update":
            entity = tokens[1] if len(tokens) > 1 else None
            target = tokens[2] if len(tokens) > 2 else None

            if "field" in tokens:
                i = tokens.index("field")
                if i + 2 < len(tokens):
                    field = tokens[i + 1]
                    value = tokens[i + 2]

            if "of" in tokens:
                i = tokens.index("of")
                if i + 2 < len(tokens):
                    relation = {
                        "relation": "of",
                        "target_type": tokens[i + 1],
                        "target": tokens[i + 2],
                    }

        # =========================
        # LINK
        # =========================
        elif action == "link":
            entity = tokens[1] if len(tokens) > 1 else None
            target = tokens[2] if len(tokens) > 2 else None

            if "to" in tokens:
                i = tokens.index("to")
                if i + 2 < len(tokens):
                    relation = {
                        "relation": "to",
                        "target_type": tokens[i + 1],
                        "target": tokens[i + 2],
                    }

        # =========================
        # QUERY OPS
        # =========================
        elif action in {"show", "exists", "schema", "missing_fields"}:
            entity = tokens[1] if len(tokens) > 1 else None
            target = tokens[2] if len(tokens) > 2 else None

        # =========================
        # FINAL AST
        # =========================
        return Command(
            action=action,
            entity=entity,
            target=target,
            field=field,
            value=value,
            relation=relation,
            context={
                "raw_tokens": tokens
            }
        )

    # =========================
    # PUBLIC API
    # =========================

    def parse(self, text: str) -> Command:
        logger.info("📩 DSL INPUT | %s", text)

        try:
            tokens = self._tokenize(text)
            command = self._to_command(tokens)

        except Exception as e:
            logger.warning("⚠️ Parse failed | %s", e)

            return Command(
                action="query",
                entity=None,
                target=None,
                field=None,
                value=None,
                relation=None,
                context={"error": str(e)}
            )

        logger.info(
            "✅ AST | action=%s entity=%s target=%s",
            command.action,
            command.entity,
            command.target
        )

        return command