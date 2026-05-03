# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Semantic intent parser (object + name + context extraction, AI-driven game indexing)

import logging
import json
import re
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (semantic mode)")

    # =========================
    # SAFE JSON EXTRACTION
    # =========================
    def _extract_json(self, text: str) -> str:
        logger.debug("🧪 Extracting JSON from AI response")

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            logger.error("❌ No JSON found in response")
            raise ValueError("No JSON found in AI response")

        return match.group(0)

    # =========================
    # MAIN PARSE
    # =========================
    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text | %s", text)

        prompt = f"""
You are a semantic game indexing parser.

Your job:
- Understand user intent in natural language
- Extract structure from sentence meaning
- Do NOT require strict schema matching

Return ONLY valid JSON.

RULES:
- object = main thing being created (building, hero, skill, item, resource)
- name = final meaningful name of the object (usually last phrase)
- context = optional relationships (hero, building, etc.)
- infer meaning from natural language

Examples:

Input:
dodaj budynek Power Plant

Output:
{{
  "action": "add_index",
  "object": "building",
  "name": "Power Plant"
}}

Input:
dodaj bohatera Tarzan

Output:
{{
  "action": "add_index",
  "object": "hero",
  "name": "Tarzan"
}}

Input:
dodaj skill bohatera Tarzan Fire Strike

Output:
{{
  "action": "add_index",
  "object": "skill",
  "name": "Fire Strike",
  "context": {{
    "hero": "Tarzan"
  }}
}}

User message:
{text}
"""

        logger.debug("🧾 Sending semantic prompt to AI")

        response = self.client.generate(prompt)

        logger.info("📨 Raw AI response received")

        try:
            raw_json = self._extract_json(response)
            data = json.loads(raw_json)

            logger.debug("📦 Parsed JSON: %s", data)

            if not isinstance(data, dict):
                logger.error("❌ AI returned non-object JSON")
                raise ValueError("Invalid AI response format")

            # =========================
            # REQUIRED FIELDS
            # =========================
            required = ["action", "object", "name"]

            for field in required:
                if field not in data or not data[field]:
                    logger.error("❌ Missing field: %s", field)
                    raise ValueError(f"Missing field: {field}")

            # =========================
            # VALIDATION
            # =========================
            if data["action"] != "add_index":
                logger.error("❌ Invalid action: %s", data["action"])
                raise ValueError("Invalid action")

            # =========================
            # CONTEXT NORMALIZATION
            # =========================
            if "context" in data and not isinstance(data["context"], dict):
                logger.warning("⚠️ Invalid context format, resetting")
                data["context"] = {}

            # =========================
            # FINAL LOG
            # =========================
            logger.info(
                "✅ Intent parsed | object=%s name=%s context=%s",
                data.get("object"),
                data.get("name"),
                data.get("context"),
            )

            return data

        except Exception as e:
            logger.error("❌ Intent parsing failed: %s", e)
            logger.error("🔎 RAW RESPONSE: %s", response)
            raise