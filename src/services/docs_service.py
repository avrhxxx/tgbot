# src/services/docs_service.py
# GROUP: services
# DESCRIPTION: Business logic for Google Docs (clean DI architecture, no client creation)

import logging

from src.google.docs.client import GoogleDocsClient
from src.google.drive.client import GoogleDriveClient
from src.google.docs.templates.hero import build_hero_template

logger = logging.getLogger("services.docs")


class DocsService:

    def __init__(
        self,
        docs_client: GoogleDocsClient,
        drive_client: GoogleDriveClient,
    ):
        # 🔥 dependency injection (NO creation inside service)
        self.client = docs_client
        self.drive = drive_client

        logger.info("📦 DocsService initialized (DI MODE)")

    # =========================
    # HERO DOCUMENT FLOW
    # =========================
    async def create_hero_document(self, name: str):

        logger.info("📄 Creating HERO doc | %s", name)

        # =========================
        # 1. DRIVE FOLDER (IDEMPOTENT)
        # =========================
        folder_id = await self.drive.ensure_folder("heroes")

        logger.info("📁 Using folder | heroes → %s", folder_id)

        # =========================
        # 2. DUPLICATE CHECK
        # =========================
        existing = await self.drive.find_file(folder_id, name)

        if existing:
            logger.info("⚠️ Hero already exists | %s → %s", name, existing)

            return {
                "doc_id": existing,
                "name": name,
                "type": "hero",
                "status": "existing",
            }

        # =========================
        # 3. BUILD CONTENT
        # =========================
        content = build_hero_template(name)

        # =========================
        # 4. CREATE DOC
        # =========================
        doc_id = await self.client.create_document(
            title=f"Hero - {name}",
            content=content,
            folder_id=folder_id,
        )

        logger.info("✅ HERO DOC CREATED | %s", doc_id)

        return {
            "doc_id": doc_id,
            "name": name,
            "type": "hero",
            "status": "created",
        }