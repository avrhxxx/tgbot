# src/wiki/scraping/content_fetcher.py
# GROUP: wiki.scraping
# DESCRIPTION: Advanced web content extractor for RAG ingestion pipeline (cleaning + chunking + heuristics)

import logging
import re
from typing import Optional, List

import aiohttp
from bs4 import BeautifulSoup  # type: ignore

logger = logging.getLogger("wiki.scraping.content_fetcher")


class ContentFetcher:
    """
    Production-ready content fetcher for RAG pipeline.

    Features:
    - async HTTP fetching (session reuse)
    - main content extraction (heuristics)
    - aggressive HTML cleanup
    - normalization
    - chunking for embeddings
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None

    # =========================
    # SESSION MANAGEMENT
    # =========================
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session and not self._session.closed:
            return self._session

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        self._session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            },
        )

        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    # =========================
    # MAIN FETCH
    # =========================
    async def fetch(self, url: str) -> Optional[str]:
        if not url:
            return None

        try:
            html = await self._download(url)

            if not html:
                return None

            text = self._extract_main_content(html)

            cleaned = self._clean(text)

            if len(cleaned) < 50:
                logger.warning("Content too short after cleaning: %s", url)
                return None

            logger.info("✅ Fetched content len=%s url=%s", len(cleaned), url)

            return cleaned

        except Exception as e:
            logger.exception("Fetch failed: %s (%s)", url, e)
            return None

    # =========================
    # DOWNLOAD HTML
    # =========================
    async def _download(self, url: str) -> Optional[str]:
        session = await self._get_session()

        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning("Bad status %s for %s", resp.status, url)
                    return None

                return await resp.text()

        except Exception as e:
            logger.warning("Download error for %s: %s", url, e)
            return None

    # =========================
    # MAIN CONTENT EXTRACTION
    # =========================
    def _extract_main_content(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # remove junk
        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "iframe",
        ]):
            tag.decompose()

        # try to find main content
        candidates = []

        for selector in ["article", "main"]:
            found = soup.select(selector)
            candidates.extend(found)

        # fallback: biggest div
        if not candidates:
            divs = soup.find_all("div")
            if divs:
                candidates.append(max(divs, key=lambda d: len(d.get_text())))

        if candidates:
            content = max(candidates, key=lambda el: len(el.get_text()))
        else:
            content = soup

        text = content.get_text(separator=" ")

        return text

    # =========================
    # CLEANING
    # =========================
    def _clean(self, text: str) -> str:
        # remove references like [1], [23]
        text = re.sub(r"\[\d+\]", "", text)

        # remove URLs inside text
        text = re.sub(r"http\S+", "", text)

        # normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # remove garbage symbols
        text = re.sub(r"[^\w\s.,!?()\-\:]", "", text)

        text = text.strip()

        # cap size (cost control)
        return text[:15000]

    # =========================
    # CHUNKING (CRITICAL FOR RAG)
    # =========================
    def chunk(self, text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
        """
        Splits text into overlapping chunks for embeddings.

        Why:
        - improves semantic recall
        - avoids losing context in long pages
        """

        if not text:
            return []

        chunks = []
        start = 0
        length = len(text)

        while start < length:
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append(chunk)

            start += chunk_size - overlap

        logger.info("📦 Chunked into %s parts", len(chunks))

        return chunks