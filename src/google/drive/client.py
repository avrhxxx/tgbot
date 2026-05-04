# src/google/drive/client.py
# GROUP: google.drive
# DESCRIPTION: Google Drive abstraction layer (folders + file management)

import logging
from typing import Optional, Any

from googleapiclient.discovery import build  # type: ignore[import-untyped]
from google.oauth2.credentials import Credentials

from src.google.auth import load_google_credentials
from src.config.config import load_config

logger = logging.getLogger("google.drive")


class GoogleDriveClient:

    def __init__(self):
        credentials: Credentials = load_google_credentials()

        self.service = build("drive", "v3", credentials=credentials)

        # =========================
        # ROOT FOLDER CONFIG
        # =========================
        config = load_config()
        self.root_folder_id = config.google.drive_root_folder_id

        logger.info("📦 GoogleDriveClient initialized")

    # =========================
    # FOLDER HELPERS (CORE)
    # =========================
    async def ensure_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Ensures folder exists, returns folder_id
        """

        # =========================
        # ROOT FALLBACK
        # =========================
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
            folder_id: str = str(files[0]["id"])
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

    # =========================
    # COMPAT LAYER (BOOTSTRAP SAFE)
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

        result = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = result.get("files", [])

        if not files:
            return None

        return str(files[0]["id"])