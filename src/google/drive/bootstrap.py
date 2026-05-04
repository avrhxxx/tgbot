# src/google/drive/bootstrap.py
# GROUP: google.drive
# DESCRIPTION: Ensures game folder structure exists in Drive

import logging
from src.google.drive.client import GoogleDriveClient
from src.config.config import load_config

logger = logging.getLogger("google.drive.bootstrap")


class DriveBootstrap:

    def __init__(self):
        self.client = GoogleDriveClient()
        self.config = load_config()

    async def ensure_structure(self):

        root_id = self.config.google.drive_root_folder_id

        if not root_id:
            raise ValueError("Missing GOOGLE_DRIVE_ROOT_FOLDER_ID")

        logger.info("📁 Bootstrapping Drive structure...")

        heroes = await self.client.create_folder("Heroes", root_id)
        items = await self.client.create_folder("Items", root_id)
        buildings = await self.client.create_folder("Buildings", root_id)
        research = await self.client.create_folder("Research", root_id)

        return {
            "heroes": heroes,
            "items": items,
            "buildings": buildings,
            "research": research,
        }