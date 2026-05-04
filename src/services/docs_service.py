# src/services/docs_service.py
# GROUP: services
# DESCRIPTION: Business logic for Google Docs knowledge generation

import logging

from src.google.docs.client import GoogleDocsClient
from src.google.docs.templates.hero import build_hero_template

logger = logging.getLogger("services.docs")


class DocsService:

    def __init__(self):
        self.client = GoogleDocsClient()
        logger.info("📦 DocsService initialized")

    # =========================
    # HERO DOCUMENT
    # =========================
    async def create_hero_document(self, name: str):

        logger.info("📄 Creating HERO doc | %s", name)

        content = build_hero_template(name)

        doc_id = await self.client.create_document(
            title=f"Hero - {name}",
            content=content,
        )

        logger.info("✅ Hero doc created | %s", doc_id)

        return {
            "doc_id": doc_id,
            "name": name,
            "type": "hero",
        }