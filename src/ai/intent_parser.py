# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: STRICT DSL Intent Parser v2 (Admin AI Engine - deterministic, schema-based)

import logging
import json
import re
from typing import Dict, Any, Optional

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:
    """
    DSL ENGINE v2

    Rules:
    - NO semantic guessing
    - STRICT token parsing
    - quoted strings = entities
    - unquoted tokens = actions / fields / values
    """

    # =========================
    # ALLOWED DSL CONFIG
    # =========================

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

    ALLOWED_ENTITIES = {
        "hero",
        "skill",
        "item",
        "building",
        "research_tree",
        "research_node",
    }

    ALLOWED_FIELDS = {
        # HERO CORE
        "hero_attack",
        "hero_defense",
        "hero_health",
        "march_capacity",
        "star_level",
        "faction",
        "troop_type",
        "lore",

        # SKILL
        "skill_damage",
        "skill_cooldown",
        "skill_level",
        "description",

        # GENERIC
        "value",
    }

    RELATION_KEYWORDS = {"of", "to", "to_hero", "to_tree", "to_building"}

    # =========================
    # INIT
    # =========================

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser v2 (DSL ENGINE) initialized")

    # =========================
    # UTIL: QUOTES EXTRACT
    # =========================

    def _extract_quoted(self, text: str) -> list:
        return re.findall(r'"([^"]+)"', text)

    def _strip_quotes(self, text: str) -> str:
        return text.replace('"', "")

    # =========================
    # TOKENIZER
    # =========================

    def _tokenize(self, text: str) -> list:
        """
        Converts DSL string into tokens while preserving quoted strings.
        """
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
    # PARSER CORE
    # =========================

    def _parse_tokens(self, tokens: list) -> Dict[str, Any]:

        if not tokens:
            raise ValueError("Empty DSL input")

        action = tokens[0]

        if action not in self.ALLOWED_ACTIONS:
            raise ValueError(f"Invalid action: {action}")

        result = {
            "action": action,
            "entity": None,
            "name": None,
            "field": None,
            "value": None,
            "target": None,
        }

        # =========================
        # CREATE / DEFINE / ADD
        # =========================

        if action in {"create", "define", "add"}:
            if len(tokens) < 3:
                raise ValueError("Invalid create/define/add syntax")

            result["entity"] = tokens[1]
            result["name"] = tokens[2]

            # optional field/value
            if "field" in tokens:
                idx = tokens.index("field")
                if idx + 2 < len(tokens):
                    result["field"] = tokens[idx + 1]
                    result["value"] = tokens[idx + 2]

            # relation handling
            for i, t in enumerate(tokens):
                if t in self.RELATION_KEYWORDS and i + 2 < len(tokens):
                    result["target"] = {
                        "type": tokens[i + 1],
                        "name": tokens[i + 2],
                    }

            return result

        # =========================
        # UPDATE
        # =========================

        if action == "update":
            if len(tokens) < 4:
                raise ValueError("Invalid update syntax")

            result["entity"] = tokens[1]
            result["name"] = tokens[2]

            # pattern: field X value Y
            if "field" in tokens:
                idx = tokens.index("field")
                if idx + 2 < len(tokens):
                    field = tokens[idx + 1]
                    value = tokens[idx + 2]

                    if field not in self.ALLOWED_FIELDS:
                        raise ValueError(f"Invalid field: {field}")

                    result["field"] = field
                    result["value"] = value

            # relation: update skill "X" of hero "Y"
            if "of" in tokens:
                idx = tokens.index("of")
                if idx + 2 < len(tokens):
                    result["target"] = {
                        "type": tokens[idx + 1],
                        "name": tokens[idx + 2],
                    }

            return result

        # =========================
        # LINK
        # =========================

        if action == "link":
            result["entity"] = tokens[1]
            result["name"] = tokens[2]

            if "to" in tokens:
                idx = tokens.index("to")
                if idx + 2 < len(tokens):
                    result["target"] = {
                        "type": tokens[idx + 1],
                        "name": tokens[idx + 2],
                    }

            return result

        # =========================
        # SHOW / EXISTS / SCHEMA
        # =========================

        if action in {"show", "exists", "schema", "missing_fields"}:
            result["entity"] = tokens[1] if len(tokens) > 1 else None
            result["name"] = tokens[2] if len(tokens) > 2 else None
            return result

        return result

    # =========================
    # PUBLIC API
    # =========================

    def parse(self, text: str) -> Dict[str, Any]:
        logger.info("📩 DSL INPUT | %s", text)

        try:
            tokens = self._tokenize(text)
            data = self._parse_tokens(tokens)

        except Exception as e:
            logger.warning("⚠️ DSL parse failed | %s", e)

            return {
                "action": "query",
                "entity": None,
                "name": None,
                "field": None,
                "value": None,
                "target": None,
                "error": str(e),
            }

        logger.info(
            "✅ Parsed | action=%s entity=%s name=%s field=%s",
            data.get("action"),
            data.get("entity"),
            data.get("name"),
            data.get("field"),
        )

        return data