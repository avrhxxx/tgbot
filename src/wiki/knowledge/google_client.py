# src/wiki/knowledge/google_client.py
# GROUP: wiki
# DESCRIPTION: Lightweight Google search layer (snippet-based, no scraping)

import logging
import aiohttp

logger = logging.getLogger("wiki.google")

GOOGLE_SEARCH_URL = "https://www.google.com/search"


async def google_search(query: str) -> list[str]:
    """
    Lightweight search (MVP version).
    NOTE: returns raw HTML snippets (later upgrade to SerpAPI or custom engine)
    """

    params = {
        "q": f"Tiles Survive {query}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GOOGLE_SEARCH_URL, params=params, headers=headers) as resp:
                html = await resp.text()

        # MVP: we do NOT parse fully yet
        # later: BeautifulSoup + structured results

        return [html[:1500]]

    except Exception as e:
        logger.exception("Google search failed: %s", e)
        return []