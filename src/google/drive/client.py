# src/google/drive/client.py
# GROUP: google.drive
# DESCRIPTION: Google Drive folder manager (for Docs organization)

import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from googleapiclient.discovery import build  # type: ignore
from src.google.auth import load_google_credentials

logger = logging.getLogger("google.drive")

_executor = ThreadPoolExecutor(max_workers=5)


class GoogleDriveClient:

    def __init__(self):
        credentials = load_google_credentials()

        self.service = build(
            "drive",
            "v3",
            credentials=credentials,
            cache_discovery=False,
        )

        logger.info("📁 Google Drive client initialized")

    async def _run(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

    # =========================
    # CREATE FOLDER
    # =========================
    async def create_folder(self, name: str, parent_id: str | None = None):

        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            metadata["parents"] = [parent_id]

        folder = await self._run(
            self.service.files().create,
            body=metadata,
            fields="id",
        )

        folder_id = folder.get("id")

        logger.info("📁 Folder created | %s -> %s", name, folder_id)

        return folder_id