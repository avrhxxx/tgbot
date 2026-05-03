# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (production-grade, region fallback, stable model)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import load_service_account

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production Vertex AI Gemini client.

    Features:
    - service account auth
    - EU-first region
    - fallback region
    - stable Gemini 2.5 model
    """

    def __init__(self):

        # =========================
        # AUTH
        # =========================
        self.credentials = load_service_account()
        self.project_id = self.credentials.project_id

        # =========================
        # MODEL CONFIG (UPDATED)
        # =========================
        self.model_name = "gemini-2.5-flash"

        # =========================
        # INIT VERTEX AI (PRIMARY REGION)
        # =========================
        self._init_vertex(region="europe-west4")

        self.model = GenerativeModel(self.model_name)

        logger.info(
            "🤖 GeminiClient initialized | project=%s model=%s region=eu",
            self.project_id,
            self.model_name,
        )

    # =========================
    # INIT HELPER
    # =========================
    def _init_vertex(self, region: str):
        vertexai.init(
            project=self.project_id,
            location=region,
            credentials=self.credentials,
        )

    # =========================
    # REGION FALLBACK
    # =========================
    def _switch_region_if_needed(self):
        try:
            self._init_vertex(region="us-central1")
            self.model = GenerativeModel(self.model_name)

            logger.warning("🌍 Vertex fallback activated → us-central1")

        except Exception as e:
            logger.exception("❌ Region fallback failed: %s", e)

    # =========================
    # GENERATION
    # =========================
    def generate(self, prompt: str) -> str:

        logger.info("🧠 Vertex AI request | model=%s", self.model_name)

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                return "Error: empty AI response"

            return str(text)

        except Exception as e:
            msg = str(e)

            # 🔥 auto recovery
            if "NOT_FOUND" in msg or "does not have access" in msg:
                logger.warning("⚠️ Model/region issue → fallback triggered")
                self._switch_region_if_needed()

                try:
                    response = self.model.generate_content(prompt)
                    return str(getattr(response, "text", ""))
                except Exception as e2:
                    logger.exception("❌ Fallback failed: %s", e2)
                    return f"AI error (fallback failed): {str(e2)}"

            logger.exception("❌ Vertex AI error: %s", e)
            return f"AI error: {str(e)}"


# =========================
# SINGLETON (KEEP)
# =========================

gemini_client = GeminiClient()