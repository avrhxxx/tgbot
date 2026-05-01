# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client for Wiki Bot (production LLM layer)

import logging
from typing import Any

import vertexai
from vertexai.generative_models import GenerativeModel

from src.config.config import load_config
from src.google.auth import load_service_account

logger = logging.getLogger("ai.gemini")

config = load_config()


# =========================
# GEMINI CLIENT (VERTEX AI)
# =========================

class GeminiClient:
    """
    Production Vertex AI Gemini client (Google Cloud authenticated).
    """

    def __init__(self):
        # =========================
        # LOAD SERVICE ACCOUNT
        # =========================
        self.credentials = load_service_account()

        # =========================
        # INIT VERTEX AI
        # =========================
        vertexai.init(
            project=config.google.service_account.get("project_id"),
            location="us-central1",
            credentials=self.credentials,
        )

        # =========================
        # MODEL (VERTEX VERSION)
        # =========================
        self.model = GenerativeModel("gemini-1.5-pro")

    async def generate(self, prompt: str) -> str:
        """
        Sends prompt to Vertex AI Gemini and returns response text.
        """

        logger.info("Sending request to Vertex AI Gemini")

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                logger.error("Empty Vertex response")
                return "Error: empty AI response"

            logger.info("Vertex AI response received")

            return str(text)

        except Exception as e:
            logger.exception("Vertex AI error: %s", e)
            return f"AI error: {str(e)}"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()