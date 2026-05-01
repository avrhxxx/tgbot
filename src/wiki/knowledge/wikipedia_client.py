# src/wiki/knowledge/wikipedia_client.py
# GROUP: wiki
# DESCRIPTION: Wikipedia API client (free + stable knowledge source for RAG)

import logging
from typing import Any, cast

import aiohttp

logger = logging.getLogger("wiki.wikipedia")

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"


def _extract_summary(data: dict[str, Any]) -> str:
    """
    Extracts clean summary from Wikipedia response.
    """
    return str(data.get("extract", "")).strip()


async def fetch_wikipedia(query: str) -> list[str]:
    """
    Fetches Wikipedia summary for a given query.
    Returns structured snippets for RAG context.
    """

    params: dict[str, str | int] = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "redirects": 1,
        "titles": query,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                WIKI_API_URL,
                params=cast(dict[str, str | int], params),
            ) as resp:

                if resp.status != 200:
                    logger.warning("Wikipedia HTTP error: %s", resp.status)
                    return []

                data: dict[str, Any] = await resp.json()

        pages = data.get("query", {}).get("pages", {})

        results: list[str] = []

        for page in pages.values():
            text = _extract_summary(page)
            if text and len(text) > 80:
                results.append(text[:800])

        logger.info("Wikipedia results: %s", len(results))

        return results[:5]

    except Exception as e:
        logger.exception("Wikipedia fetch failed: %s", e)
        return []