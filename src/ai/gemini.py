# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (fixed model name + stable runtime)

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
    Production Vertex AI Gemini client.
    """

    def __init__(self):
        # =========================
        # AUTH
        # =========================
        self.credentials = load_service_account()
        project_id = self.credentials.project_id

        # =========================
        # INIT VERTEX
        # =========================
        vertexai.init(
            project=project_id,
            location="us-central1",
            credentials=self.credentials,
        )

        # =========================
        # MODEL (FIXED)
        # =========================
        # IMPORTANT:
        # DO NOT use gemini-2.x publisher paths unless explicitly enabled
        self.model = GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt: str) -> str:
        """
        Sync call (wrapped by async layer in service).
        """

        logger.info("Sending request to Vertex AI Gemini")

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                logger.error("Empty Vertex response")
                return "Error: empty AI response"

            return str(text)

        except Exception as e:
            logger.exception("Vertex AI error: %s", e)
            return f"AI error: {str(e)}"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()