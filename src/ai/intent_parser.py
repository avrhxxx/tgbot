# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Vertex AI intent parser (clean contract, no computed fields)

import logging
import json
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized")

    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text for parsing | text=%s", text)

        prompt = f"""
You are a strict command parser.

Return ONLY valid JSON.

Allowed action:
- add_index

Allowed types:
- building
- hero
- item
- resource

User message:
{text}

Output format:
{{
  "action": "add_index",
  "type": "building",
  "name": "Power Plant"
}}
"""

        logger.debug("🧾 Sending prompt to Gemini")

        response = self.client.generate(prompt)

        logger.info("📨 Raw AI response received")

        try:
            data = json.loads(response)

            if not isinstance(data, dict):
                raise ValueError("AI returned invalid JSON")

            # ------------------------
            # REQUIRED FIELDS CHECK
            # ------------------------
            required = ["action", "type", "name"]

            for field in required:
                if field not in data:
                    logger.error("❌ Missing field: %s", field)
                    raise ValueError(f"Missing field: {field}")

            logger.info(
                "✅ Intent parsed | action=%s type=%s name=%s",
                data.get("action"),
                data.get("type"),
                data.get("name"),
            )

            return data

        except Exception:
            logger.error("❌ Intent parsing failed")
            logger.error("🔎 RAW RESPONSE: %s", response)
            raise