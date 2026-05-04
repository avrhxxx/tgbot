# src/google/drive/client.py
# GROUP: google.drive
# DESCRIPTION: Google Drive abstraction layer (folders + stable root support)

import logging
from typing import Optional, Any

from googleapiclient.discovery import build  # type: ignore
from src.google.auth import load_google_credentials
from src.config.config import load_config

logger = logging.getLogger("google.drive")


class GoogleDriveClient:

    create_folder: Any  # ✅ FIX: satisfies mypy static checker

    def __init__(self):
        credentials = load_google_credentials()

        logger.info("📁 Drive AUTH EMAIL: %s", getattr(credentials, "service_account_email", None))

        self.service = build("drive", "v3", credentials=credentials, cache_discovery=False)

        config = load_config()
        self.root_folder_id = config.google.drive_root_folder_id

        logger.info("📦 GoogleDriveClient initialized")
        logger.info("📁 ROOT FOLDER ID: %s", self.root_folder_id)

    async def ensure_folder(self, name: str, parent_id: Optional[str] = None) -> str:

        if parent_id is None:
            parent_id = self.root_folder_id

        query = (
            f"name='{name}' and "
            f"mimeType='application/vnd.google-apps.folder' and "
            "trashed=false"
        )

        if parent_id:
            query += f" and '{parent_id}' in parents"

        result = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = result.get("files", [])

        if files:
            folder_id = str(files[0]["id"])
            logger.info("📁 Folder exists | %s → %s", name, folder_id)
            return folder_id

        metadata: dict[str, Any] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            metadata["parents"] = [str(parent_id)]

        folder = self.service.files().create(
            body=metadata,
            fields="id"
        ).execute()

        folder_id = str(folder.get("id"))

        logger.info("📁 Folder created | %s → %s", name, folder_id)

        return folder_id

    async def find_file(self, folder_id: str, name: str) -> Optional[str]:

        query = (
            f"name contains '{name}' and "
            f"'{folder_id}' in parents and "
            "trashed=false"
        )

        result = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = result.get("files", [])

        if not files:
            return None

        return str(files[0]["id"])