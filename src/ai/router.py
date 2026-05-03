# src/ai/router.py
# GROUP: ai
# DESCRIPTION: AI request router (WRITE intent vs READ query classifier)

import logging
from dataclasses import dataclass
from typing import Literal, Dict, Any

from google import genai
from google.genai import types

from src.config.config import load_config

logger = logging.getLogger("ai.router")


Mode = Literal["write", "read"]


@dataclass
class RouteResult:
    mode: Mode
    payload: Dict[str, Any]


class AIRouter:

    def __init__(self):
        config = load_config()

        self.api_key = config.gemini.api_key
        if not self.api_key:
            raise RuntimeError("Missing GEMINI_API_KEY")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"

        logger.info("🧠 AI Router initialized")

    def route(self, text: str) -> RouteResult:
        """
        Decides if request is:
        - WRITE (index creation/modification)
        - READ (querying game knowledge)
        """

        prompt = f"""
You are a strict router for a game database system.

Return ONLY valid JSON:

{
  "mode": "write" or "read",
  "data": object
}

RULES:
- "write" = adding or modifying game entities (hero, skill, building)
- "read" = questions about existing data (how many, what exists, list)

USER INPUT:
{text}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    max_output_tokens=256,
                ),
            )

            raw = response.text.strip()

            logger.info("📦 Router raw response: %s", raw)

            import json
            data = json.loads(raw)

            return RouteResult(
                mode=data["mode"],
                payload=data.get("data", {})
            )

        except Exception as e:
            logger.exception("❌ Router failed")

            # SAFE fallback → assume WRITE (safer for your system)
            return RouteResult(
                mode="write",
                payload={
                    "fallback": True,
                    "raw": text
                }
            )