# src/wiki/knowledge/google_client.py
# GROUP: wiki
# DESCRIPTION: Google Custom Search API client (production-safe structured search)

import logging
import aiohttp

from src.config.config import load_config

logger = logging.getLogger("wiki.google")

config = load_config()

GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"


def _format_results(items: list[dict]) -> list[str]:
    """
    Formats Google API results into clean text snippets.
    """

    results: list[str] = []

    for item in items:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")

        combined = f"{title}\n{snippet}\n{link}".strip()

        if combined:
            results.append(combined)

    return results[:5]


async def google_search(query: str) -> list[str]:
    """
    Production Google Search using Custom Search API.
    """

    api_key = config.google.search.api_key
    cx = config.google.search.cx

    if not api_key or not cx:
        logger.error("Google Search API not configured")
        return []

    params = {
        "key": api_key,
        "cx": cx,
        "q": f"Tiles Survive {query}",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GOOGLE_API_URL, params=params) as resp:

                if resp.status != 200:
                    logger.warning("Google API HTTP error: %s", resp.status)
                    return []

                data = await resp.json()

        items = data.get("items", [])

        results = _format_results(items)

        logger.info("Google results: %s", len(results))

        return results

    except Exception as e:
        logger.exception("Google search failed: %s", e)
        return []