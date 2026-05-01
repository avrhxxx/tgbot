# src/wiki/knowledge/google_client.py
# GROUP: wiki
# DESCRIPTION: Safe search layer (DuckDuckGo lightweight structured snippets)

import logging
import aiohttp

logger = logging.getLogger("wiki.google")

DDG_URL = "https://duckduckgo.com/html/"


def _extract_snippets(html: str) -> list[str]:
    """
    Lightweight fallback HTML parsing (no external dependencies).
    """

    results: list[str] = []

    # very naive but CI-safe extraction
    blocks = html.split("result__body")

    for block in blocks:
        if "result__title" in block and "result__snippet" in block:

            # crude text extraction (MVP fallback)
            text = block.replace("<", " <").replace(">", "> ")

            if len(text) > 80:
                results.append(text[:300])

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