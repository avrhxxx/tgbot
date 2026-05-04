# src/google/drive/client.py
# GROUP: google.drive
# DESCRIPTION: Google Drive client (GAME_DATA root + document creation layer)

import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials

logger = logging.getLogger("google.drive")


class DriveClient:
    """
    Minimal Drive layer:
    - ensures root folder exists (provided via env)
    - creates documents inside GAME_DATA
    """

    def __init__(self, credentials: Credentials, root_folder_id: str):
        self.service = build("drive", "v3", credentials=credentials)
        self.root_folder_id = root_folder_id

        logger.info("📁 DriveClient initialized | root=%s", root_folder_id)

    # =========================
    # CREATE DOCUMENT
    # =========================
    def create_document(self, name: str, content: str, parent_id: Optional[str] = None):
        """
        Creates a Google Doc inside Drive.

        If parent_id not provided → uses GAME_DATA root.
        """

        folder_id = parent_id or self.root_folder_id

        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [folder_id],
        }

        media = MediaInMemoryUpload(
            content.encode("utf-8"),
            mimetype="text/plain",
        )

        file = (
            self.service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id, name",
            )
            .execute()
        )

        logger.info("📄 Document created | name=%s id=%s", name, file["id"])

        return file

    # =========================
    # FIND FOLDER BY NAME (optional utility later)
    # =========================
    def list_children(self, folder_id: str):
        """
        Debug helper: lists files in folder.
        """
        res = (
            self.service.files()
            .list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, mimeType)",
            )
            .execute()
        )

        return res.get("files", [])