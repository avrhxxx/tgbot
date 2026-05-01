# src/wiki/knowledge/google_client.py
# GROUP: wiki
# DESCRIPTION: Safe search layer (DuckDuckGo lightweight structured snippets)

import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger("wiki.google")

DDG_URL = "https://duckduckgo.com/html/"


def _extract_snippets(html: str) -> list[str]:
    """
    Extract search snippets from DuckDuckGo HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    results = []

    for a in soup.select(".result__body"):
        title = a.select_one(".result__title")
        snippet = a.select_one(".result__snippet")

        if title and snippet:
            text = f"{title.get_text(strip=True)} - {snippet.get_text(strip=True)}"
            results.append(text)

    return results[:5]


async def google_search(query: str) -> list[str]:
    """
    Safe search layer (replaces Google scraping).
    """

    params = {
        "q": f"Tiles Survive {query}"
    }

    headers = {
        "User-Agent": "tiles-survive-wiki-bot/1.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DDG_URL, params=params, headers=headers) as resp:
                html = await resp.text()

        results = _extract_snippets(html)

        logger.info("Search results: %s", len(results))

        return results

    except Exception as e:
        logger.exception("Search failed: %s", e)
        return []