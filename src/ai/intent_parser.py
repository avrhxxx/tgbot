# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Semantic intent parser (INDEX + KNOWLEDGE dual system, extended learning)

import logging
import json
import re
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (learning mode v3)")

    # =========================
    # JSON EXTRACTION
    # =========================
    def _extract_json(self, text: str) -> str:
        """
        Extracts JSON block from LLM response.
        More robust than greedy regex.
        """
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON found in AI response")
        return match.group(0)

    # =========================
    # NORMALIZATION
    # =========================
    def _normalize_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:

        if "object" not in data and "type" in data:
            data["object"] = data["type"]

        if "context" not in data or data["context"] is None:
            data["context"] = {}

        if "action" not in data:
            data["action"] = "query"

        # =========================
        # KNOWLEDGE STRUCTURE ENFORCEMENT
        # =========================
        if data.get("action") == "add_knowledge":
            if "knowledge" not in data:
                data["knowledge"] = {}

            knowledge = data["knowledge"]

            # Safe defaults (NO dict-in-string bugs)
            knowledge.setdefault("lore", "")
            knowledge.setdefault("gameplay", {
                "type": None,
                "behavior": None
            })
            knowledge.setdefault("stats", {})

        return data

    # =========================
    # VALIDATION
    # =========================
    def _validate(self, data: Dict[str, Any]) -> None:

        allowed_actions = {
            "query",
            "check_existence",
            "get_definition",
            "add_definition",   # INDEX SYSTEM
            "add_knowledge",    # KNOWLEDGE SYSTEM
            "add_tree",
            "add_tree_research"
        }

        if data.get("action") not in allowed_actions:
            raise ValueError(f"Invalid action: {data.get('action')}")

    # =========================
    # MAIN PARSE
    # =========================
    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text | %s", text)

        prompt = f"""
You are a GAME INTELLIGENCE ENGINE.

You handle TWO SYSTEMS:

=================================
1. INDEX SYSTEM (Sheets)
=================================
- add_definition → creates game entities
- includes: hero, skill, building, item
- ALSO includes:
  • research_tree
  • research_node

RULE:
- INDEX = existence only
- NEVER include mechanics or behavior

=================================
2. KNOWLEDGE SYSTEM (Firestore)
=================================
- add_knowledge = structured game intelligence

MUST FOLLOW STRUCTURE:

{{
  "lore": "string",
  "gameplay": {{
    "type": "passive | active | auto_attack | talent",
    "behavior": "string",
    "cooldown": optional,
    "levels": optional
  }},
  "stats": {{
    "damage": optional,
    "scaling": optional,
    "duration": optional
  }}
}}

=================================
3. READ SYSTEM
=================================
- check_existence
- get_definition
- query

=================================
RULES
=================================
- NEVER mix INDEX and KNOWLEDGE
- INDEX = structure of game
- KNOWLEDGE = meaning + behavior
- ALWAYS return valid JSON ONLY

=================================
USER INPUT
=================================
{text}
"""

        response = self.client.generate(prompt)

        try:
            raw_json = self._extract_json(response)
            data = json.loads(raw_json)

            data = self._normalize_schema(data)
            self._validate(data)

            logger.info(
                "✅ Intent | action=%s object=%s name=%s",
                data.get("action"),
                data.get("object"),
                data.get("name"),
            )

            return data

        except Exception as e:
            logger.error("❌ Intent parse failed: %s", e)
            logger.error("RAW: %s", response)
            raise