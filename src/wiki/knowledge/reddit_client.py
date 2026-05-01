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
    Uses public JSON endpoint with anti-block headers.
    """

    url = f"https://www.reddit.com/r/{SUBREDDIT}/search.json"

    params: dict[str, str] = {
        "q": query,
        "restrict_sr": "1",
        "sort": "relevance",
        "limit": str(limit),
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        ),
        "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:

                # 🔴 FIX: Reddit sometimes returns HTML on block
                if resp.status != 200:
                    logger.warning("Reddit HTTP error: %s", resp.status)
                    return []

                content_type = resp.headers.get("Content-Type", "")

                if "application/json" not in content_type:
                    logger.warning("Reddit returned non-JSON: %s", content_type)
                    return []

                data = await resp.json()

        results: list[str] = []

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