# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (production-safe + stable model routing)

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
    Production Vertex AI Gemini client (stable + fallback-safe).
    """

    def __init__(self):
        # =========================
        # AUTH
        # =========================
        self.credentials = load_service_account()

        project_id = getattr(self.credentials, "project_id", None)

        if not project_id:
            raise RuntimeError("Missing project_id in Google credentials")

        # =========================
        # INIT VERTEX
        # =========================
        vertexai.init(
            project=project_id,
            location="us-central1",
            credentials=self.credentials,
        )

        # =========================
        # MODEL ROUTING (STABLE)
        # =========================
        self.model_name = "gemini-2.0-flash-001"

        try:
            self.model = GenerativeModel(self.model_name)
            logger.info("Using Vertex model: %s", self.model_name)

        except Exception as e:
            logger.warning(
                "Primary model failed (%s), falling back: %s",
                self.model_name,
                e,
            )

            # fallback (safer option)
            self.model_name = "gemini-2.0-flash-lite-001"
            self.model = GenerativeModel(self.model_name)

            logger.info("Fallback Vertex model: %s", self.model_name)

    def generate(self, prompt: str) -> str:
        """
        Blocking Vertex call (safe wrapper for async layer).
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