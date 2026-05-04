# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (ADC-only, no service account coupling)

import logging
import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import get_vertex_credentials
from src.config.config import load_config

logger = logging.getLogger("ai.gemini")


class GeminiClient:

    def __init__(self):

        logger.info("🤖 Initializing GeminiClient (ADC ONLY)...")

        config = load_config()

        self.project_id = config.google.project_id

        if not self.project_id:
            raise RuntimeError("Missing GCP project_id")

        # =========================
        # ADC ONLY
        # =========================
        self.credentials = get_vertex_credentials()

        self.model_name = "gemini-2.5-flash"

        self._init_vertex()

        self.model = GenerativeModel(self.model_name)

        logger.info("🧠 Gemini ready | model=%s", self.model_name)

        self._health_check()

    def _init_vertex(self):
        vertexai.init(
            project=self.project_id,
            location="europe-west4",
            credentials=self.credentials,
        )

    def _health_check(self):
        logger.info("🧪 Vertex AI health check...")

        res = self.model.generate_content("ping")

        if not getattr(res, "text", None):
            raise RuntimeError("Vertex AI health check failed")

        logger.info("✅ Vertex AI OK")

    def generate(self, prompt: str) -> str:

        try:
            response = self.model.generate_content(prompt)
            return str(response.text or "")

        except Exception as e:
            logger.error("❌ Gemini error: %s", e)
            return f"AI error: {e}"


gemini_client = GeminiClient()