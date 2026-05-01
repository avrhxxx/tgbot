# src/wiki/knowledge/fandom_client.py
# GROUP: wiki
# DESCRIPTION: Fandom wiki knowledge layer for Tiles Survive

import logging
import aiohttp

logger = logging.getLogger("wiki.fandom")

BASE_URL = "https://tiles-survive.fandom.com/wiki/"


async def fetch_fandom_page(query: str) -> str:
    """
    Simple Fandom page fetcher (best-effort MVP).
    NOTE: In production should use proper wiki API parsing.
    """

    page_name = query.strip().replace(" ", "_")
    url = f"{BASE_URL}{page_name}"

    headers = {
        "User-Agent": "tiles-survive-wiki-bot/1.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                html = await resp.text()

        # crude extraction (MVP only)
        # later: BeautifulSoup / structured parser

        if len(html) > 2000:
            return html[:2000]

        return html

    except Exception as e:
        logger.exception("Fandom fetch failed: %s", e)
        return ""