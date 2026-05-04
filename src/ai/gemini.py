# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (Service Account, production-safe, non-crashing)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

from src.config.config import load_config

logger = logging.getLogger("ai.gemini")


class GeminiClient:
    """
    Production-ready Gemini client.

    - uses Service Account (works outside GCP)
    - does NOT crash app on init failure
    - has region fallback
    """

    def __init__(self):

        logger.info("🤖 Initializing GeminiClient (SERVICE ACCOUNT)...")

        config = load_config()

        cred_dict = config.google.service_account

        if not cred_dict:
            raise RuntimeError("❌ Missing GOOGLE_SERVICE_ACCOUNT")

        self.project_id = cred_dict.get("project_id")

        if not self.project_id:
            raise RuntimeError("❌ Missing project_id in GOOGLE_SERVICE_ACCOUNT")

        logger.info("📦 Gemini project_id: %s", self.project_id)

        # =========================
        # SERVICE ACCOUNT CREDS (🔥 FIX)
        # =========================
        self.credentials = service_account.Credentials.from_service_account_info(
            cred_dict,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        self.model_name = "gemini-2.5-flash"
        self.model = None

        # =========================
        # INIT
        # =========================
        self._init_vertex(region="europe-west4")

        # =========================
        # HEALTH CHECK (SAFE)
        # =========================
        self._safe_health_check()

    # =========================
    # INIT
    # =========================
    def _init_vertex(self, region: str):
        logger.info("⚙️ Initializing Vertex AI | region=%s", region)

        try:
            vertexai.init(
                project=self.project_id,
                location=region,
                credentials=self.credentials,
            )

            self.model = GenerativeModel(self.model_name)

            logger.info("✅ Vertex initialized | region=%s", region)

        except Exception as e:
            logger.exception("❌ Vertex init failed: %s", e)
            self.model = None

    # =========================
    # HEALTH CHECK (SAFE - NO CRASH)
    # =========================
    def _safe_health_check(self):
        logger.info("🧪 Vertex AI health check...")

        if not self.model:
            logger.error("❌ Model not initialized")
            return

        try:
            res = self.model.generate_content("ping")

            if not getattr(res, "text", None):
                raise RuntimeError("Empty response")

            logger.info("✅ Vertex AI OK")

        except Exception as e:
            logger.warning("⚠️ Health check failed, trying fallback region...")

            # fallback region
            self._init_vertex(region="us-central1")

            try:
                if self.model:
                    res = self.model.generate_content("ping")
                    logger.info("✅ Vertex fallback OK")
                else:
                    logger.error("❌ Fallback init failed")

            except Exception as e2:
                logger.exception("❌ Vertex completely unavailable: %s", e2)

    # =========================
    # GENERATION
    # =========================
    def generate(self, prompt: str) -> str:

        logger.info("🧠 Gemini request | model=%s", self.model_name)

        if not self.model:
            return "AI error: model not initialized"

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