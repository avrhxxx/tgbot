# src/ai/intent_parser.py
# GROUP: ai
# DESCRIPTION: Vertex AI strict intent parser (NL → structured index schema)

import logging
import json
from typing import Dict, Any

from src.ai.gemini import GeminiClient

logger = logging.getLogger("ai.intent_parser")


class IntentParser:
    """
    Strict converter: natural language → structured index command.
    """

    def __init__(self):
        self.client = GeminiClient()
        logger.info("🧠 IntentParser initialized (GeminiClient ready)")

    # =========================
    # MAIN PARSE PIPELINE
    # =========================
    def parse(self, text: str) -> Dict[str, Any]:

        logger.info("📩 Incoming text for parsing | text=%s", text)

        # =========================
        # PROMPT (STRICT SCHEMA)
        # =========================
        prompt = f"""
You are a STRICT JSON generator for a game indexing system.

RULES:
- Output ONLY valid JSON
- No markdown
- No explanation
- No extra fields

ALLOWED ACTIONS:
- add_index

ALLOWED TYPES:
- building
- hero
- item
- resource

OUTPUT SCHEMA:
{{
  "action": "add_index",
  "type": "<building|hero|item|resource>",
  "name": "<original name>",
  "normalized": "<snake_case lowercase name>"
}}

NORMALIZATION RULES:
- lowercase
- spaces → underscores
- remove special characters

EXAMPLE:
Input:
add building Power Plant

Output:
{{
  "action": "add_index",
  "type": "building",
  "name": "Power Plant",
  "normalized": "power_plant"
}}

USER INPUT:
{text}
"""

        logger.debug("🧾 Sending prompt to AI")

        response = self.client.generate(prompt)

        logger.info("📨 Raw AI response received")
        logger.debug("🧠 AI RAW: %s", response)

        # =========================
        # PARSE + VALIDATE
        # =========================
        try:
            data = json.loads(response)

            logger.debug("🔎 Parsed JSON: %s", data)

            if not isinstance(data, dict):
                logger.error("❌ AI response is not a dict")
                raise ValueError("Invalid AI response format")

            # =========================
            # REQUIRED FIELD SAFETY
            # =========================
            required = ["action", "type", "name", "normalized"]

            for field in required:
                if field not in data:
                    logger.error("❌ Missing field in AI response: %s", field)
                    raise ValueError(f"Missing field: {field}")

            logger.info(
                "✅ AI intent parsed successfully | action=%s type=%s name=%s normalized=%s",
                data.get("action"),
                data.get("type"),
                data.get("name"),
                data.get("normalized"),
            )

            return data

        except json.JSONDecodeError as e:
            logger.error("❌ JSON decode failed")
            logger.error("🔎 RAW RESPONSE: %s", response)
            logger.exception(e)
            raise

        except Exception as e:
            logger.error("❌ Intent parsing failed")
            logger.error("🔎 RAW RESPONSE: %s", response)
            logger.exception(e)
            raise