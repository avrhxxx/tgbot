# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (production-grade, Railway-safe, health-checked)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

from src.config.config import load_config

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production Vertex AI Gemini client.

    Features:
    - service account auth (proper Credentials object)
    - EU-first region + fallback
    - Gemini 2.5 Flash stable model
    - startup health-check (warm-up request)
    """

    def __init__(self):

        logger.info("🤖 Initializing GeminiClient...")

        # =========================
        # CONFIG LOAD
        # =========================
        config = load_config()

        cred_dict = config.google.service_account

        if not cred_dict:
            raise RuntimeError("❌ Missing GOOGLE_SERVICE_ACCOUNT")

        self.project_id = cred_dict.get("project_id")

        if not self.project_id:
            raise RuntimeError("❌ Missing project_id in GOOGLE_SERVICE_ACCOUNT")

        # =========================
        # CREDENTIALS (FIXED)
        # =========================
        self.credentials = service_account.Credentials.from_service_account_info(
            cred_dict
        )

        logger.info("🔐 Credentials loaded successfully")
        logger.info("📦 Project ID: %s", self.project_id)

        # =========================
        # MODEL CONFIG
        # =========================
        self.model_name = "gemini-2.5-flash"

        # =========================
        # INIT VERTEX AI
        # =========================
        self._init_vertex(region="europe-west4")

        self.model = GenerativeModel(self.model_name)

        logger.info("🌍 Vertex AI initialized in region: europe-west4")
        logger.info("🧠 Model selected: %s", self.model_name)

        # =========================
        # HEALTH CHECK (IMPORTANT)
        # =========================
        self._health_check()

    # =========================
    # INIT HELPER
    # =========================
    def _init_vertex(self, region: str):
        logger.info("⚙️ Initializing Vertex AI | region=%s", region)

        vertexai.init(
            project=self.project_id,
            location=region,
            credentials=self.credentials,
        )

    # =========================
    # HEALTH CHECK
    # =========================
    def _health_check(self):
        logger.info("🧪 Running Vertex AI health check...")

        try:
            test = self.model.generate_content("ping")

            if not getattr(test, "text", None):
                raise RuntimeError("Empty response during health check")

            logger.info("✅ Vertex AI HEALTH CHECK PASSED")

        except Exception as e:
            logger.exception("❌ Vertex AI HEALTH CHECK FAILED")
            raise RuntimeError(f"Vertex AI not ready: {e}") from e

    # =========================
    # REGION FALLBACK
    # =========================
    def _switch_region_if_needed(self):

        logger.warning("🌍 Switching Vertex region → us-central1")

        try:
            self._init_vertex(region="us-central1")
            self.model = GenerativeModel(self.model_name)

            logger.warning("✅ Fallback region active: us-central1")

        except Exception as e:
            logger.exception("❌ Region fallback failed: %s", e)

    # =========================
    # GENERATION
    # =========================
    def generate(self, prompt: str) -> str:

        logger.info("🧠 Gemini request | model=%s", self.model_name)

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                logger.error("❌ Empty AI response")
                return "Error: empty AI response"

            return str(text)

        except Exception as e:
            msg = str(e)

            logger.error("❌ Vertex AI error: %s", msg)

            if "NOT_FOUND" in msg or "does not have access" in msg:
                logger.warning("⚠️ Triggering region fallback...")
                self._switch_region_if_needed()

                try:
                    response = self.model.generate_content(prompt)
                    return str(getattr(response, "text", ""))
                except Exception as e2:
                    logger.exception("❌ Fallback failed: %s", e2)
                    return f"AI error (fallback failed): {str(e2)}"

            return f"AI error: {str(e)}"


# =========================
# SINGLETON
# =========================

gemini_client = GeminiClient()