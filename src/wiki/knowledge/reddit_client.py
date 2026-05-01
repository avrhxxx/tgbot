# src/wiki/knowledge/reddit_client.py
# GROUP: wiki
# DESCRIPTION: Reddit knowledge layer for Tiles Survive wiki bot (MVP + safe parsing)

import logging
import aiohttp

logger = logging.getLogger("wiki.reddit")

SUBREDDIT = "tilessurvive"


async def search_reddit(query: str, limit: int = 5) -> list[str]:
    """
    Fetches Reddit posts related to Tiles Survive.
    Uses public JSON endpoint (no API key required).
    """

    url = f"https://www.reddit.com/r/{SUBREDDIT}/search.json"

    params = {
        "q": query,
        "restrict_sr": 1,
        "sort": "relevance",
        "limit": limit
    }

    headers = {
        "User-Agent": "tiles-survive-wiki-bot/1.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                data = await resp.json()

        results = []

        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})

            title = post.get("title", "")
            text = post.get("selftext", "")

            if title:
                combined = f"{title}\n{text}".strip()
                results.append(combined)

        logger.info("Reddit results: %s", len(results))
        return results

    except Exception as e:
        logger.exception("Reddit fetch failed: %s", e)
        return []