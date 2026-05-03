# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Minimal Gemini client stub (MVP safe)

import logging

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Temporary stub client.

    Later: Vertex AI / Gemini API integration
    """

    def __init__(self):
        logger.info("🤖 GeminiClient initialized (stub mode)")

    def generate(self, prompt: str) -> str:
        logger.info("🧠 Gemini prompt received (stub mode)")

        # MVP fallback (no AI dependency yet)
        return """
        {
          "action": "add_index",
          "type": "building",
          "name": "Power Plant"
        }
        """