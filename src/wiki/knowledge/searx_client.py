# src/wiki/knowledge/searx_client.py
# GROUP: wiki
# DESCRIPTION: SearXNG metasearch client (replaces DDG scraping, RAG-ready)

import logging
import httpx

logger = logging.getLogger("wiki.searx")

DEFAULT_TIMEOUT = 10


class SearxClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, limit: int = 5) -> list[str]:
        """
        Performs metasearch using SearXNG JSON API.
        """

        url = f"{self.base_url}/search"

        params = {
            "q": query,
            "format": "json",
        }

        try:
            async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
                r = await client.get(url, params=params)
                r.raise_for_status()
                data = r.json()

            results = data.get("results", [])[:limit]

            output = []

            for r in results:
                title = r.get("title") or ""
                snippet = r.get("content") or ""
                link = r.get("url") or ""

                if not title and not snippet:
                    continue

                text = f"{title} - {snippet}".strip()

                if link:
                    text += f" ({link})"

                if len(text) > 40:
                    output.append(text[:800])

            logger.info("SearX results: %s", len(output))

            return output

        except Exception as e:
            logger.exception("SearX search failed: %s", e)
            return []