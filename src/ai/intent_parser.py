# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Semantic intent parser (INDEX + KNOWLEDGE + DOCS intent compiler)

import logging
import json
import re
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (strict intent compiler mode)")

    # =========================
    # JSON EXTRACTION
    # =========================
    def _extract_json(self, text: str) -> str:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON found in AI response")
        return match.group(0)

    # =========================
    # FALLBACK (CRITICAL)
    # =========================
    def _fallback_parse(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        # ===== CREATE DOCUMENT =====
        if "dokument" in text_lower or "document" in text_lower:
            name = text.split()[-1]

            if "bohater" in text_lower or "hero" in text_lower:
                return {
                    "action": "create_document",
                    "object": "hero",
                    "name": name,
                    "context": {}
                }

            if "item" in text_lower:
                return {
                    "action": "create_document",
                    "object": "item",
                    "name": name,
                    "context": {}
                }

        # ===== ADD INDEX =====
        if "dodaj bohater" in text_lower:
            name = text.split()[-1]
            return {
                "action": "add_definition",
                "object": "hero",
                "name": name,
                "context": {}
            }

        return {
            "action": "query",
            "object": None,
            "name": None,
            "context": {}
        }

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
        # KNOWLEDGE SAFETY DEFAULTS
        # =========================
        if data.get("action") == "add_knowledge":
            knowledge = data.get("knowledge", {})

            knowledge.setdefault("lore", "")
            knowledge.setdefault("gameplay", {
                "type": None,
                "behavior": None
            })
            knowledge.setdefault("stats", {})

            data["knowledge"] = knowledge

        return data

    # =========================
    # VALIDATION
    # =========================
    def _validate(self, data: Dict[str, Any]) -> None:

        allowed_actions = {
            "query",
            "check_existence",
            "get_definition",

            # INDEX SYSTEM
            "add_definition",

            # KNOWLEDGE SYSTEM
            "add_knowledge",

            # TREE SYSTEM
            "add_tree",
            "add_tree_research",

            # DOCS (UPDATED)
            "create_document",
        }

        if data.get("action") not in allowed_actions:
            raise ValueError(f"Invalid action: {data.get('action')}")

    # =========================
    # MAIN PARSE
    # =========================
    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text | %s", text)

        prompt = f"""
You are a STRICT INTENT COMPILER.

You convert user input into CLEAN JSON ACTIONS.

You DO NOT execute anything.
You DO NOT know APIs.
You ONLY output intent.

=================================
OUTPUT RULES (HARD CONSTRAINT)
=================================

- Output MUST be valid JSON ONLY
- NO markdown
- NO explanation
- NO extra keys
- NO guessing fields
- ALWAYS full schema compliance

=================================
ACTION TYPES
=================================

1. add_definition (INDEX SYSTEM)
2. add_knowledge (KNOWLEDGE SYSTEM)
3. check_existence
4. get_definition
5. query
6. create_document (DOCS INTENT)

=================================
INDEX SYSTEM
=================================

{{
  "action": "add_definition",
  "object": "hero | skill | item | building | research_tree | research_node",
  "name": "string",
  "context": {{}}
}}

=================================
KNOWLEDGE SYSTEM
=================================

{{
  "action": "add_knowledge",
  "object": "hero | skill | item | building",
  "name": "string",
  "knowledge": {{
    "lore": "string",
    "gameplay": {{
      "type": "passive | active | auto_attack | talent",
      "behavior": "string",
      "cooldown": 0,
      "levels": 0
    }},
    "stats": {{
      "damage": 0,
      "scaling": "string",
      "duration": 0
    }}
  }}
}}

=================================
DOCS INTENT (GENERIC)
=================================

This does NOT create files directly.

It only requests backend action:

{{
  "action": "create_document",
  "object": "hero | building | item | skill",
  "name": "string"
}}

=================================
RULES
=================================

- NEVER output API calls
- NEVER mention Google Drive or Docs
- NEVER change schema dynamically
- ALWAYS prefer fixed enum values

=================================
USER INPUT
=================================
{text}
"""

        try:
            response = self.client.generate(prompt)

            raw_json = self._extract_json(response)
            data = json.loads(raw_json)

        except Exception as e:
            logger.warning("⚠️ AI failed, using fallback | %s", e)
            data = self._fallback_parse(text)

        data = self._normalize_schema(data)
        self._validate(data)

        logger.info(
            "✅ Intent | action=%s object=%s name=%s",
            data.get("action"),
            data.get("object"),
            data.get("name"),
        )

        return data