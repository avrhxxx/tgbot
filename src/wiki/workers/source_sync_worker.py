# src/wiki/workers/source_sync_worker.py
# GROUP: wiki.workers
# DESCRIPTION: Background worker syncing Google Sheets sources → Firestore RAG pipeline

import asyncio
import logging
from typing import Any, Dict

from src.google.sheets.client import GoogleSheetsClient
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.wiki.embeddings.client import EmbeddingClient

logger = logging.getLogger("wiki.worker.source_sync")


class SourceSyncWorker:
    """
    Background ingestion pipeline:

    Google Sheets (NEW links)
        ↓
    Fetch content (scraper)
        ↓
    Embeddings (async safe)
        ↓
    Firestore (RAG storage)
        ↓
    Mark DONE in Sheets

    Features:
    - deduplication (Firestore-level)
    - async-safe embedding
    - retry handled in Sheets client
    - audit-friendly logging
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
        Runs forever until stop() is called.
        """

        if self.running:
            logger.warning("Worker already running")
            return

        self.running = True
        logger.info("🚀 SourceSyncWorker started (interval=%ss)", interval)

        try:
            while self.running:
                try:
                    await self.sync_once()

                except Exception as e:
                    logger.exception("❌ Sync cycle failed: %s", e)

                await asyncio.sleep(interval)

        finally:
            logger.info("🛑 Worker loop exited")

    # =========================
    # STOP
    # =========================
    def stop(self):
        self.running = False
        logger.info("🛑 SourceSyncWorker stop requested")

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
            if not self.running:
                logger.info("Worker stopping mid-cycle")
                return

            await self.process_source(item)

        logger.info("✅ Sync cycle finished")

    # =========================
    # PROCESS SINGLE SOURCE
    # =========================
    async def process_source(self, item: Dict[str, Any]):
        row = item["row"]
        url = item["url"]
        topic = item.get("topic", "unknown")

        logger.info("📥 Processing row=%s url=%s topic=%s", row, url, topic)

        try:
            # ---------------------------------
            # 0. DUPLICATE CHECK (IMPORTANT)
            # ---------------------------------
            exists = await self.firestore.source_exists(url)

            if exists:
                logger.info("⏭ Skipping existing source: %s", url)
                self.sheets.mark_done(row)
                return

            # ---------------------------------
            # 1. FETCH CONTENT
            # ---------------------------------
            content = await self.fetch_content(url)

            if not content or len(content.strip()) < 20:
                raise ValueError("Content too short or empty")

            logger.info("📄 Content length: %s", len(content))

            # ---------------------------------
            # 2. EMBEDDING (NON-BLOCKING)
            # ---------------------------------
            loop = asyncio.get_event_loop()

            embedding = await loop.run_in_executor(
                None,
                self.embedder.embed,
                content,
            )

            if not embedding:
                raise ValueError("Embedding failed")

            logger.info("🧠 Embedding generated (%s dims)", len(embedding))

            # ---------------------------------
            # 3. STORE IN FIRESTORE
            # ---------------------------------
            created = await self.firestore.add_knowledge(
                topic=topic,
                url=url,
                content=content,
                embedding=embedding,
            )

            if not created:
                logger.info("⚠️ Firestore skipped (duplicate): %s", url)

            # ---------------------------------
            # 4. MARK DONE
            # ---------------------------------
            self.sheets.mark_done(row)

            logger.info("✅ DONE row=%s url=%s", row, url)

            # ---------------------------------
            # 5. RATE LIMIT (ANTI-429)
            # ---------------------------------
            await asyncio.sleep(1.0)

        except Exception as e:
            logger.exception("❌ Failed processing row=%s url=%s: %s", row, url, e)

            try:
                self.sheets.mark_error(row)
            except Exception as err:
                logger.exception("❌ Failed to mark error in Sheets: %s", err)

    # =========================
    # CONTENT FETCH (TEMP)
    # =========================
    async def fetch_content(self, url: str) -> str:
        """
        TEMP placeholder scraper.

        TODO:
        - integrate content_fetcher.py
        - strip HTML
        - extract main article text
        - chunk large content
        """

        logger.warning("⚠️ Using placeholder fetch_content for: %s", url)

        return f"content-from:{url}"