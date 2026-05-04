# src/google/drive/bootstrap.py
# GROUP: google.drive
# DESCRIPTION: Ensures game folder structure exists in Drive (stable, single-source API usage)

import logging
from src.google.drive.client import GoogleDriveClient
from src.config.config import load_config

logger = logging.getLogger("google.drive.bootstrap")


class DriveBootstrap:

    def __init__(self):
        self.client = GoogleDriveClient()
        self.config = load_config()

        logger.info("🧩 DriveBootstrap initialized")
        logger.info("🧪 Drive client class: %s", self.client.__class__.__name__)
        logger.info("🧪 Drive methods: %s", [m for m in dir(self.client) if not m.startswith("_")])

    async def ensure_structure(self):

        root_id = self.config.google.drive_root_folder_id

        if not root_id:
            raise ValueError("Missing GOOGLE_DRIVE_ROOT_FOLDER_ID")

        logger.info("📁 Bootstrapping Drive structure...")
        logger.info("📌 Root folder ID: %s", root_id)

        # =========================
        # SAFE FOLDER CREATION (SINGLE SOURCE OF TRUTH)
        # =========================

        heroes = await self.client.ensure_folder("Heroes", root_id)
        items = await self.client.ensure_folder("Items", root_id)
        buildings = await self.client.ensure_folder("Buildings", root_id)
        research = await self.client.ensure_folder("Research", root_id)

        structure = {
            "heroes": heroes,
            "items": items,
            "buildings": buildings,
            "research": research,
        }

        logger.info("📂 Drive structure initialized:")

        for name, folder_id in structure.items():
            logger.info("   - %s → %s", name, folder_id)

        logger.info("✅ Drive bootstrap completed successfully")

        return structure