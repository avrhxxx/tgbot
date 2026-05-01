# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (multi-region + stable model)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import load_service_account

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production Vertex AI Gemini client with safe model + region fallback.
    """

    def __init__(self):

        # =========================
        # AUTH
        # =========================
        self.credentials = load_service_account()
        project_id = self.credentials.project_id

        # =========================
        # INIT VERTEX AI (EU FIRST)
        # =========================
        vertexai.init(
            project=project_id,
            location="europe-west4",
            credentials=self.credentials,
        )

        # =========================
        # MODEL (CURRENT STABLE)
        # =========================
        self.model_name = "gemini-2.5-flash"

        self.model = GenerativeModel(self.model_name)

    def _switch_region_if_needed(self):
        """
        Optional fallback if EU model not available.
        """
        try:
            vertexai.init(
                project=self.credentials.project_id,
                location="us-central1",
                credentials=self.credentials,
            )
            self.model = GenerativeModel(self.model_name)
            logger.warning("Switched Vertex region to us-central1 fallback")

        except Exception as e:
            logger.exception("Region fallback failed: %s", e)

    def generate(self, prompt: str) -> str:

        logger.info("Sending request to Vertex AI Gemini")

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                return "Error: empty AI response"

            return str(text)

        except Exception as e:

            msg = str(e)

            # 🔥 auto fallback on region/model issues
            if "NOT_FOUND" in msg or "does not have access" in msg:
                logger.warning("Model/region issue detected, retrying fallback...")
                self._switch_region_if_needed()

                try:
                    response = self.model.generate_content(prompt)
                    return str(getattr(response, "text", ""))
                except Exception as e2:
                    logger.exception("Fallback failed: %s", e2)
                    return f"AI error (fallback failed): {str(e2)}"

            logger.exception("Vertex AI error: %s", e)
            return f"AI error: {str(e)}"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()