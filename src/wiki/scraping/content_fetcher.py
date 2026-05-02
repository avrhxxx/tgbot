# src/wiki/scraping/content_fetcher.py
# GROUP: wiki.scraping
# DESCRIPTION: Lightweight web content extractor for RAG ingestion pipeline

import logging
import re
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup  # type: ignore

logger = logging.getLogger("wiki.scraping.content_fetcher")


class ContentFetcher:
    """
    Fetches and cleans webpage content for embedding pipeline.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout

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

            text = self._extract_text(html)

            cleaned = self._clean(text)

            return cleaned

        except Exception as e:
            logger.exception("Fetch failed: %s (%s)", url, e)
            return None

    # =========================
    # DOWNLOAD HTML
    # =========================
    async def _download(self, url: str) -> Optional[str]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning("Bad status %s for %s", resp.status, url)
                    return None

                return await resp.text()

    # =========================
    # HTML → TEXT
    # =========================
    def _extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # remove junk
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        return text

    # =========================
    # CLEANING
    # =========================
    def _clean(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\[\d+\]", "", text)  # wiki refs
        text = text.strip()

        # safety cap (embedding cost control)
        return text[:12000]