# src/wiki/knowledge/reddit_client.py
# GROUP: wiki
# DESCRIPTION: Reddit knowledge layer for Tiles Survive wiki bot

import aiohttp
import logging

logger = logging.getLogger("wiki.reddit")

SUBREDDIT = "tilessurvive"


async def search_reddit(query: str) -> list[str]:
    """
    Fetches top Reddit posts related to Tiles Survive.
    MVP version: uses public JSON endpoint (no API key needed)
    """

    url = f"https://www.reddit.com/r/{SUBREDDIT}/search.json"

    params = {
        "q": query,
        "restrict_sr": 1,
        "sort": "relevance",
        "limit": 5
    }

    headers = {
        "User-Agent": "tiles-survive-wiki-bot/1.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                data = await resp.json()

        posts = []

        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            title = post.get("title")
            selftext = post.get("selftext", "")

            if title:
                posts.append(f"{title}\n{selftext}")

        return posts

    except Exception as e:
        logger.exception("Reddit fetch failed: %s", e)
        return []