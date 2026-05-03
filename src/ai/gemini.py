# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Production Gemini client (Google Generative AI API)

import logging
import os
from typing import Optional

from google import genai
from google.genai import types

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production Gemini client using Google Generative AI API.

    Requires:
    - GOOGLE_API_KEY in environment
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

        self.client = genai.Client(api_key=self.api_key)

        self.model = "gemini-1.5-flash"

        logger.info("🤖 GeminiClient initialized (PRODUCTION MODE)")

    # =========================
    # GENERATION
    # =========================
    def generate(self, prompt: str) -> str:
        logger.info("🧠 Sending request to Gemini API")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=512,
                ),
            )

            text = response.text.strip()

            logger.info("📨 Gemini response received (%s chars)", len(text))

            return text

        except Exception as e:
            logger.exception("❌ Gemini API call failed")
            raise RuntimeError(f"Gemini API error: {e}") from e