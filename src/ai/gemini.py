# src/ai/gemini.py
# GROUP: ai
# DESCRIPTION: Vertex AI Gemini client (region + model fixed)

import logging

import vertexai
from vertexai.generative_models import GenerativeModel

from src.google.auth import load_service_account

logger = logging.getLogger("ai.gemini")


class GeminiClient:

    def __init__(self):

        # AUTH
        self.credentials = load_service_account()
        project_id = self.credentials.project_id

        # IMPORTANT: match your EU setup
        vertexai.init(
            project=project_id,
            location="europe-west4",
            credentials=self.credentials,
        )

        # STABLE MODEL (Vertex-safe)
        self.model = GenerativeModel("gemini-1.5-pro")

    def generate(self, prompt: str) -> str:

        logger.info("Sending request to Vertex AI Gemini")

        try:
            response = self.model.generate_content(prompt)

            text = getattr(response, "text", None)

            if not text:
                return "Error: empty AI response"

            return str(text)

        except Exception as e:
            logger.exception("Vertex AI error: %s", e)
            return f"AI error: {str(e)}"


gemini_client = GeminiClient()