# src/google/docs/client.py
# GROUP: google.docs
# DESCRIPTION: Google Docs API client (async-safe, minimal writer)

import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from googleapiclient.discovery import build  # type: ignore
from google.cloud import firestore  # noqa (only for auth reuse)
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
    async def create_document(self, title: str, content: str) -> str:
        """
        Creates a Google Doc and writes full content.
        Returns document ID.
        """

        doc = await self._run(
            self.service.documents().create,
            body={"title": title},
        )

        doc_id = doc.get("documentId")

        logger.info("📄 Doc created | id=%s | title=%s", doc_id, title)

        await self._write_content(doc_id, content)

        return doc_id

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