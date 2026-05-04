# src/services/docs_service.py
# GROUP: services
# DESCRIPTION: Business logic for Google Docs knowledge generation

import logging

from src.google.docs.client import GoogleDocsClient
from src.google.docs.templates.hero import build_hero_template
from src.google.drive.client import GoogleDriveClient  # 🔥 DODANE

logger = logging.getLogger("services.docs")


class DocsService:

    def __init__(self):
        self.client = GoogleDocsClient()
        self.drive = GoogleDriveClient()  # 🔥 DODANE
        logger.info("📦 DocsService initialized")

    # =========================
    # HERO DOCUMENT
    # =========================
    async def create_hero_document(self, name: str):

        logger.info("📄 Creating HERO doc | %s", name)

        # =========================
        # 1. ENSURE FOLDER STRUCTURE
        # =========================
        folder_id = await self.drive.ensure_folder("heroes")

        # =========================
        # 2. CHECK DUPLICATE (IDEMPOTENCY)
        # =========================
        existing = await self.drive.find_file(folder_id, name)

        if existing:
            logger.info("⚠️ Hero already exists | %s", name)
            return {
                "doc_id": existing,
                "name": name,
                "type": "hero",
                "status": "existing"
            }

        # =========================
        # 3. BUILD TEMPLATE
        # =========================
        content = build_hero_template(name)

        # =========================
        # 4. CREATE DOC IN FOLDER
        # =========================
        doc_id = await self.client.create_document(
            title=f"Hero - {name}",
            content=content,
            folder_id=folder_id  # 🔥 KLUCZOWE
        )

        logger.info("✅ Hero doc created | %s", doc_id)

        return {
            "doc_id": doc_id,
            "name": name,
            "type": "hero",
            "status": "created"
        }