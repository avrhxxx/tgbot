# src/wiki/workers/source_sync_worker.py
# GROUP: wiki.workers
# DESCRIPTION: Background worker syncing Google Sheets sources → Firestore RAG pipeline

import asyncio
import logging
from typing import Any, Dict, List

from src.google.sheets.client import GoogleSheetsClient
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.wiki.embeddings.client import EmbeddingClient

logger = logging.getLogger("wiki.worker.source_sync")


class SourceSyncWorker:
    """
    Background ingestion pipeline:

    Google Sheets (NEW links)
        ↓
    Fetch content (future scraper step)
        ↓
    Embeddings
        ↓
    Firestore RAG store
        ↓
    Mark DONE in Sheets
    """

    def __init__(
        self,
        sheets: GoogleSheetsClient,
        firestore: FirestoreClient,
        embedder: EmbeddingClient,
    ):
        self.sheets = sheets
        self.firestore = firestore
        self.embedder = embedder

        self.running = False

    # =========================
    # START LOOP
    # =========================
    async def start(self, interval: int = 30):
        """
        Main background loop.
        """
        self.running = True

        logger.info("🚀 SourceSyncWorker started")

        # ensure sheet structure exists
        self.sheets.ensure_structure()

        while self.running:
            try:
                await self.sync_once()

            except Exception as e:
                logger.exception("Sync cycle failed: %s", e)

            await asyncio.sleep(interval)

    # =========================
    # STOP
    # =========================
    def stop(self):
        self.running = False
        logger.info("🛑 SourceSyncWorker stopped")

    # =========================
    # SINGLE SYNC CYCLE
    # =========================
    async def sync_once(self):
        logger.info("🔄 Sync cycle started")

        sources = self.sheets.fetch_new_sources()

        if not sources:
            logger.info("No new sources")
            return

        logger.info("Found %s new sources", len(sources))

        for item in sources:
            await self.process_source(item)

        logger.info("✅ Sync cycle finished")

    # =========================
    # PROCESS SINGLE SOURCE
    # =========================
    async def process_source(self, item: Dict[str, Any]):
        row = item["row"]
        url = item["url"]
        topic = item.get("topic", "unknown")

        logger.info("Processing: %s (%s)", url, topic)

        try:
            # ---------------------------------
            # 1. FETCH CONTENT (placeholder)
            # ---------------------------------
            content = await self.fetch_content(url)

            if not content:
                raise ValueError("Empty content")

            # ---------------------------------
            # 2. EMBEDDING
            # ---------------------------------
            embedding = self.embedder.embed(content)

            # ---------------------------------
            # 3. STORE IN FIRESTORE
            # ---------------------------------
            await self.firestore.add_knowledge(
                topic=topic,
                url=url,
                content=content,
                embedding=embedding,
            )

            # ---------------------------------
            # 4. MARK DONE
            # ---------------------------------
            self.sheets.mark_done(row)

            logger.info("✅ DONE: %s", url)

        except Exception as e:
            logger.exception("❌ Failed processing %s: %s", url, e)

            self.sheets.mark_error(row)

    # =========================
    # CONTENT FETCH (TEMP)
    # =========================
    async def fetch_content(self, url: str) -> str:
        """
        Placeholder scraper.

        TU później podepniemy:
        - BeautifulSoup scraper
        - readability-lxml
        - albo Playwright jeśli dynamiczne strony
        """

        # MVP fallback (na razie NIE crashujemy pipeline)
        return f"content-from:{url}"