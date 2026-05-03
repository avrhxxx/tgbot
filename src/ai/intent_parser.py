# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Robust semantic intent parser (AI-safe, schema-flexible, production-ready)

import logging
import json
import re
from typing import Dict, Any, Optional

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (robust semantic mode)")

    # =========================
    # JSON EXTRACTION (AI SAFE)
    # =========================
    def _extract_json(self, text: str) -> str:
        logger.debug("🧪 Extracting JSON from AI response")

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            logger.error("❌ No JSON found in AI response")
            raise ValueError("No JSON found in AI response")

        return match.group(0)

    # =========================
    # FIELD NORMALIZATION (BACKWARD COMPAT)
    # =========================
    def _normalize_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:

        # support legacy AI outputs
        if "object" not in data and "type" in data:
            logger.warning("⚠️ Mapping legacy 'type' → 'object'")
            data["object"] = data["type"]

        # ensure context exists
        if "context" not in data or data["context"] is None:
            data["context"] = {}

        return data

    # =========================
    # VALIDATION (SAFE MODE)
    # =========================
    def _validate(self, data: Dict[str, Any]) -> None:

        required = ["action", "object", "name"]

        for field in required:
            if field not in data or not data[field]:
                logger.error("❌ Missing required field: %s", field)
                raise ValueError(f"Missing field: {field}")

        if data.get("action") != "add_index":
            logger.error("❌ Invalid action: %s", data.get("action"))
            raise ValueError("Invalid action")

    # =========================
    # MAIN PARSE
    # =========================
    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text | %s", text)

        prompt = f"""
You are a semantic game indexing parser.

Your job:
- Understand intent from natural language
- Extract structured meaning
- Be flexible, not strict

Return ONLY valid JSON.

RULES:
- object = main entity (building, hero, skill, item, resource)
- name = final entity name
- context = optional relationships (hero, building, etc.)

Examples:

Input: dodaj budynek Power Plant
Output:
{{"action":"add_index","object":"building","name":"Power Plant"}}

Input: dodaj bohatera Tarzan
Output:
{{"action":"add_index","object":"hero","name":"Tarzan"}}

Input: dodaj skill bohatera Tarzan Fire Strike
Output:
{{"action":"add_index","object":"skill","name":"Fire Strike","context":{{"hero":"Tarzan"}}}}

User:
{text}
"""

        logger.debug("🧾 Sending prompt to AI")

        response = self.client.generate(prompt)

        logger.info("📨 Raw AI response received")

        try:
            raw_json = self._extract_json(response)
            data = json.loads(raw_json)

            if not isinstance(data, dict):
                logger.error("❌ AI returned non-dict JSON")
                raise ValueError("Invalid AI response format")

            # normalize schema BEFORE validation
            data = self._normalize_schema(data)

            # validate required fields
            self._validate(data)

            logger.info(
                "✅ Intent parsed | object=%s name=%s context_keys=%s",
                data.get("object"),
                data.get("name"),
                list(data.get("context", {}).keys()) if data.get("context") else []
            )

            return data

        except Exception as e:
            logger.error("❌ Intent parsing failed: %s", e)
            logger.error("🔎 RAW RESPONSE: %s", response)
            raise