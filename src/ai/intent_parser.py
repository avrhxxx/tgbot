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
        match = re.search(r"\{.*\}", text, re.DOTALL)
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

        # BACKWARD COMPATIBILITY (OLD SYSTEM)
        if data.get("action") == "add_definition":
            # future bridge to knowledge system (optional mapping)
            data["legacy_mode"] = True

        return data


    # =========================
    # VALIDATION
    # =========================
    def _validate(self, data: Dict[str, Any]) -> None:

        allowed_actions = {
            "query",
            "check_existence",
            "get_definition",
            "add_definition",   # 🔴 INDEX SYSTEM (UNCHANGED)
            "add_knowledge",    # 🟢 NEW KNOWLEDGE SYSTEM
            "add_tree",         # 🌲 research tree
            "add_tree_research" # 🌲 add node to tree
        }

        if data.get("action") not in allowed_actions:
            raise ValueError(f"Invalid action: {data.get('action')}")

        return None


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
- ALSO includes extended structures:
  • research_tree
  • research_node (inside tree)

Rules:
- index = existence only
- NEVER describe mechanics here

EXAMPLES:

Input: dodaj drzewko badań technologii
Output:
{{"action":"add_definition","object":"research_tree","name":"Technologia"}}

Input: dodaj badanie do drzewka Technologia: Laser Upgrade
Output:
{{
  "action":"add_definition",
  "object":"research_node",
  "name":"Laser Upgrade",
  "context":{{"tree":"Technologia"}}
}}

=================================
2. KNOWLEDGE SYSTEM (Firestore)
=================================
- add_knowledge → description layer
- explains meaning, stats, behavior

EXAMPLES:

Input: dodaj wiedzę o Fire Strike
Output:
{{
  "action":"add_knowledge",
  "object":"skill",
  "name":"Fire Strike",
  "knowledge_type":"behavior"
}}

=================================
3. READ SYSTEM
=================================

check_existence:
- verify if entity exists in INDEX

get_definition:
- retrieve Firestore knowledge

query:
- normal question

=================================
RULES
=================================

- NEVER mix INDEX and KNOWLEDGE
- INDEX = structure
- KNOWLEDGE = meaning
- ALWAYS preserve hierarchy relations

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