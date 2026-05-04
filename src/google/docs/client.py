
# src/google/docs/client.py
# GROUP: google.docs
# DESCRIPTION: Google Docs API client (async-safe, singleton-auth aware, folder-safe via Drive move)

import logging
import asyncio
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

import google.auth
from googleapiclient.discovery import build  # type: ignore

from src.google.auth import load_google_credentials

logger = logging.getLogger("google.docs")

_executor = ThreadPoolExecutor(max_workers=5)


class GoogleDocsClient:

    def __init__(self):
        credentials = load_google_credentials()

        # =========================
        # 🔍 BASIC IDENTITY DEBUG
        # =========================
        logger.info(
            "📄 Docs AUTH EMAIL: %s",
            getattr(credentials, "service_account_email", None)
            or getattr(credentials, "client_email", None),
        )

        logger.info("📄 Docs AUTH TYPE: %s", type(credentials).__name__)
        logger.info("📄 Docs CREDS OBJECT ID: %s", id(credentials))

        # =========================
        # 🔍 ADC / PROJECT DEBUG
        # =========================
        try:
            _, project = google.auth.default()
            logger.info("📄 ADC PROJECT: %s", project)
        except Exception as e:
            logger.warning("📄 ADC PROJECT CHECK FAILED: %s", e)

        # =========================
        # SERVICES
        # =========================
        self.docs_service = build(
            "docs",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

        self.drive_service = build(
            "drive",
            "v3",
            credentials=credentials,
            cache_discovery=False,
        )

        self._credentials = credentials

        logger.info("📄 Docs SERVICE READY")

    async def _run(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

    async def create_document(
        self,
        title: str,
        content: str,
        folder_id: Optional[str] = None,
    ):
        # =========================
        # 1. CREATE DOC
        # =========================
        request = self.docs_service.documents().create(body={"title": title})
        doc = await self._run(request.execute)

        doc_id = doc.get("documentId")
        if not doc_id:
            raise RuntimeError("Failed to create document")

        logger.info("📄 Doc created | id=%s | title=%s", doc_id, title)

        # =========================
        # 2. WRITE CONTENT
        # =========================
        await self._write_content(doc_id, content)

        # =========================
        # 3. MOVE TO FOLDER (🔥 CRITICAL FIX)
        # =========================
        if folder_id:
            try:
                logger.info("📁 Moving doc to folder | %s → %s", doc_id, folder_id)

                # get current parents
                file = await self._run(
                    self.drive_service.files().get,
                    fileId=doc_id,
                    fields="parents",
                )

                previous_parents = ",".join(file.get("parents", []))

                # move file
                await self._run(
                    self.drive_service.files().update,
                    fileId=doc_id,
                    addParents=folder_id,
                    removeParents=previous_parents,
                    fields="id, parents",
                )

                logger.info("✅ Doc moved to folder")

            except Exception:
                logger.exception("❌ Failed to move document to folder")

        return str(doc_id)

    async def _write_content(self, doc_id: str, content: str):
        requests = [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": content,
                }
            }
        ]

        await self._run(
            self.docs_service.documents().batchUpdate,
            documentId=doc_id,
            body={"requests": requests},
        )

        logger.info("✍️ Doc written | id=%s", doc_id)