# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Vertex AI intent parser (natural language → structured command)

import logging
import json
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:
    """
    Converts natural language into structured index commands.
    """

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (GeminiClient ready)")

    def parse(self, text: str) -> Dict[str, Any]:
        logger.info("📩 Incoming text for parsing: %s", text)

        prompt = f"""
You are a strict command parser for a game indexing system.

Return ONLY valid JSON. No markdown. No explanation.

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

        logger.debug("🧾 Sending prompt to AI")

        response = self.client.generate(prompt)

        logger.info("📨 Raw AI response received")

        try:
            data = json.loads(response)

            # ✅ safety check for mypy + runtime stability
            if not isinstance(data, dict):
                logger.error("❌ AI returned non-dict JSON")
                raise ValueError("Invalid AI response format")

            logger.info(
                "✅ Parsed AI intent successfully | action=%s type=%s name=%s",
                data.get("action"),
                data.get("type"),
                data.get("name"),
            )

            return data

        except Exception as e:
            logger.error("❌ Failed to parse AI response")
            logger.error("🔎 Raw response: %s", response)
            logger.exception(e)
            raise