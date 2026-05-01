# src/wiki/knowledge/ddg_client.py
# GROUP: wiki
# DESCRIPTION: DuckDuckGo lightweight web search (robust fallback parser)

import logging
import re
import aiohttp

logger = logging.getLogger("wiki.ddg")

DDG_URL = "https://duckduckgo.com/html/"


def _extract_snippets(html: str) -> list[str]:
    """
    More robust extraction using regex instead of brittle split.
    """

    results: list[str] = []

    # title + snippet pattern (DuckDuckGo HTML structure)
    pattern = re.compile(
        r'result__title.*?>(.*?)</a>.*?result__snippet.*?>(.*?)</a>',
        re.DOTALL
    )

    matches = pattern.findall(html)

    for title, snippet in matches:
        clean = f"{title.strip()} - {snippet.strip()}"

        # safety filter
        if len(clean) > 60:
            results.append(clean[:400])

    return results[:5]


async def search_ddg(query: str) -> list[str]:
    """
    Free web search fallback (no API key).
    """

    params = {
        "q": query
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        )
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                DDG_URL,
                params=params,
                headers=headers,
                timeout=10
            ) as resp:

                html = await resp.text()

        results = _extract_snippets(html)

        logger.info("DDG results: %s", len(results))

        return results

    except Exception as e:
        logger.exception("DDG search failed: %s", e)
        return []