# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (production-safe + correct auth + non-blocking wrapper)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import load_service_account

logger = logging.getLogger("ai.gemini")


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

        project_id = self.credentials.project_id

        # =========================
        # INIT VERTEX AI
        # =========================
        vertexai.init(
            project=project_id,
            location="us-central1",
            credentials=self.credentials,
        )

        # =========================
        # MODEL
        # =========================
        self.model = GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt: str) -> str:
        """
        Synchronous Vertex call (wrapped safely by async layer outside).
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