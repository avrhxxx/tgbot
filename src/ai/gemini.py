# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Gemini AI client for Wiki Bot (core LLM layer)

import logging
import aiohttp

from src.config.config import load_config

logger = logging.getLogger("ai.gemini")

config = load_config()


# =========================
# GEMINI CLIENT
# =========================

class GeminiClient:
    """
    Minimal async Gemini client (REST API).
    """

    def __init__(self):
        self.api_key = config.gemini.api_key
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
        )

    async def generate(self, prompt: str) -> str:
        """
        Sends prompt to Gemini and returns response text.
        """

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is missing")

        url = (
            f"{self.base_url}"
            f"gemini-1.5-flash:generateContent?key={self.api_key}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        logger.info("Sending request to Gemini")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=30) as resp:
                data = await resp.json()

                try:
                    return (
                        data["candidates"][0]["content"]["parts"][0]["text"]
                    )
                except Exception:
                    logger.exception("Invalid Gemini response format")
                    return "Error: invalid AI response"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()