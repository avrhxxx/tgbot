# src/google/drive/client.py
# GROUP: google.drive
# DESCRIPTION: Google Drive abstraction layer (folders + file management)

import logging
from typing import Optional, cast, Any

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from src.google.auth import load_google_credentials

logger = logging.getLogger("google.drive")


class GoogleDriveClient:

    def __init__(self):
        credentials: Credentials = load_google_credentials()

        self.service = build("drive", "v3", credentials=credentials)

        logger.info("📦 GoogleDriveClient initialized")

    # =========================
    # FOLDER HELPERS (CORE)
    # =========================
    async def ensure_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Ensures folder exists, returns folder_id
        """

        query = (
            f"name='{name}' and "
            f"mimeType='application/vnd.google-apps.folder' and "
            "trashed=false"
        )

        if parent_id:
            query += f" and '{parent_id}' in parents"

        result: dict[str, Any] = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = result.get("files", [])

        if files:
            folder_id = str(files[0]["id"])
            logger.info("📁 Folder exists | %s → %s", name, folder_id)
            return folder_id

        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            metadata["parents"] = [parent_id]

        folder = self.service.files().create(
            body=metadata,
            fields="id"
        ).execute()

        folder_id = str(folder.get("id"))

        logger.info("📁 Folder created | %s → %s", name, folder_id)

        return folder_id

    # =========================
    # COMPAT LAYER (FIX FOR BOOTSTRAP EXPECTATION)
    # =========================
    async def create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Alias for ensure_folder (backward compatibility)
        """
        return await self.ensure_folder(name, parent_id)

    # =========================
    # FILE SEARCH
    # =========================
    async def find_file(self, folder_id: str, name: str) -> Optional[str]:
        """
        Finds file by name in folder
        """

        query = (
            f"name contains '{name}' and "
            f"'{folder_id}' in parents and "
            "trashed=false"
        )

        result: dict[str, Any] = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = result.get("files", [])

        if not files:
            return None

        return cast(str, files[0]["id"])