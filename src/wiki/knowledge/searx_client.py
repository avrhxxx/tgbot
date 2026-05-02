# src/wiki/knowledge/searx_client.py
# GROUP: wiki
# DESCRIPTION: SearXNG metasearch client (Docker Compose ready, RAG-safe)

import logging
import httpx

logger = logging.getLogger("wiki.searx")

DEFAULT_TIMEOUT = 10


class SearxClient:
    def __init__(self, base_url: str):
        # Docker Compose internal DNS safe
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, limit: int = 5) -> list[str]:
        """
        Performs metasearch using SearXNG JSON API.
        Works in Docker Compose (service name resolution supported).
        """

        url = f"{self.base_url}/search"

        params = {
            "q": query,
            "format": "json",
        }

        timeout = httpx.Timeout(DEFAULT_TIMEOUT)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            results = data.get("results", [])[:limit]

            output: list[str] = []

            for item in results:
                title = item.get("title") or ""
                snippet = item.get("content") or ""
                link = item.get("url") or ""

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