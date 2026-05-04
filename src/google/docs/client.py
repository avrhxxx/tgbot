# src/google/docs/client.py
# GROUP: google.docs
# DESCRIPTION: Google Docs API client (async-safe, minimal writer)

import logging
import asyncio
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from googleapiclient.discovery import build  # type: ignore
from src.google.auth import load_google_credentials

logger = logging.getLogger("google.docs")

_executor = ThreadPoolExecutor(max_workers=5)


class GoogleDocsClient:
    def __init__(self):
        credentials = load_google_credentials()

        self.service = build(
            "docs",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

        logger.info("📄 Google Docs client initialized")

    # =========================
    # ASYNC WRAPPER
    # =========================
    async def _run(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

    # =========================
    # CREATE DOCUMENT
    # =========================
    async def create_document(
        self,
        title: str,
        content: str,
        folder_id: Optional[str] = None,
    ) -> str:
        """
        Creates a Google Doc and writes full content.
        Optionally can be linked to Drive folder (via move step).
        """

        request = self.service.documents().create(body={"title": title})
        doc = await self._run(request.execute)

        doc_id = doc.get("documentId")
        if not doc_id:
            raise RuntimeError("Failed to create document")

        logger.info("📄 Doc created | id=%s | title=%s", doc_id, title)

        await self._write_content(doc_id, content)

        # NOTE: folder handling is done via Drive API (optional hook)
        if folder_id:
            logger.info("📁 Linking doc to folder | doc=%s folder=%s", doc_id, folder_id)
            # future: drive move operation (kept intentionally decoupled)

        return str(doc_id)

    # =========================
    # WRITE CONTENT
    # =========================
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
            self.service.documents().batchUpdate,
            documentId=doc_id,
            body={"requests": requests},
        )

        logger.info("✍️ Doc written | id=%s", doc_id)