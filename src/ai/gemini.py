# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (production-grade, Railway-safe, config-driven)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.config.config import load_config

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production Vertex AI Gemini client.

    - config-driven auth (Railway-safe)
    - EU-first region
    - fallback region
    - Gemini 2.5 Flash stable
    """

    def __init__(self):

        # =========================
        # CONFIG
        # =========================
        config = load_config()

        self.credentials = config.google.service_account

        if not self.credentials:
            raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT config")

        self.project_id = self.credentials.get("project_id")

        if not self.project_id:
            raise RuntimeError("Missing project_id in service account")

        # =========================
        # MODEL
        # =========================
        self.model_name = "gemini-2.5-flash"

        # =========================
        # INIT VERTEX (EU FIRST)
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
# SINGLETON
# =========================

gemini_client = GeminiClient()