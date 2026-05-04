# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Semantic intent parser (learning loop + admin-controlled knowledge growth)

import logging
import json
import re
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (learning mode v2)")


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

        return data


    # =========================
    # VALIDATION (FLEXIBLE)
    # =========================
    def _validate(self, data: Dict[str, Any]) -> None:

        allowed_actions = {
            "query",
            "check_existence",
            "get_definition",
            "add_definition"
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

You do NOT just extract data.

You decide intent:

========================
ACTIONS YOU CAN RETURN
========================

1. query
- normal question about game

2. check_existence
- user asks if something exists in game (Sheets lookup)

3. get_definition
- user asks what something means (Firestore lookup)

4. add_definition
- user is adding missing knowledge
- ONLY allow if explicitly requested
- ALWAYS assume admin validation required

========================
RULES
========================
- object = hero / skill / building / item
- name = entity name
- context = relationships

========================
EXAMPLES
========================

Input: czy istnieje Tarzan
Output:
{{"action":"check_existence","object":"hero","name":"Tarzan"}}

Input: co to jest Fire Strike
Output:
{{"action":"get_definition","object":"skill","name":"Fire Strike"}}

Input: dodaj definicję Fire Strike to skill Tarzana z opisem ...
Output:
{{"action":"add_definition","object":"skill","name":"Fire Strike","context":{{"hero":"Tarzan"}}}}

User:
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