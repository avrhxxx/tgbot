# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (ADC-only, config-safe, production-ready)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import get_vertex_credentials
from src.config.config import load_config

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Vertex AI Gemini client using ADC ONLY.

    - uses ADC credentials (separate from Service Account used for Docs/Drive)
    - resolves project_id safely from config or env
    - includes health check
    """

    def __init__(self):

        logger.info("🤖 Initializing GeminiClient (ADC ONLY)...")

        config = load_config()

        # =========================
        # PROJECT ID RESOLUTION (🔥 FIX)
        # =========================
        project_id = None

        # 1. try config.google.service_account
        if config.google.service_account:
            project_id = config.google.service_account.get("project_id")

        # 2. fallback to ENV (for ADC setups)
        if not project_id:
            import os
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

        if not project_id:
            raise RuntimeError("❌ Missing project_id (service_account or GOOGLE_CLOUD_PROJECT)")

        self.project_id = project_id

        logger.info("📦 Gemini project_id: %s", self.project_id)

        # =========================
        # ADC CREDENTIALS
        # =========================
        self.credentials = get_vertex_credentials()

        self.model_name = "gemini-2.5-flash"

        # =========================
        # INIT VERTEX
        # =========================
        self._init_vertex()

        self.model = GenerativeModel(self.model_name)

        logger.info("🧠 Gemini ready | model=%s", self.model_name)

        # =========================
        # HEALTH CHECK
        # =========================
        self._health_check()

    def _init_vertex(self):
        logger.info("⚙️ Initializing Vertex AI | project=%s", self.project_id)

        vertexai.init(
            project=self.project_id,
            location="europe-west4",
            credentials=self.credentials,
        )

    def _health_check(self):
        logger.info("🧪 Vertex AI health check...")

        try:
            res = self.model.generate_content("ping")

            if not getattr(res, "text", None):
                raise RuntimeError("Empty response")

            logger.info("✅ Vertex AI OK")

        except Exception as e:
            logger.exception("❌ Vertex AI health check failed")
            raise RuntimeError(f"Vertex AI not ready: {e}") from e

    def generate(self, prompt: str) -> str:

        logger.info("🧠 Gemini request | model=%s", self.model_name)

        try:
            response = self.model.generate_content(prompt)
            return str(getattr(response, "text", "") or "")

        except Exception as e:
            logger.error("❌ Gemini error: %s", e)
            return f"AI error: {e}"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()