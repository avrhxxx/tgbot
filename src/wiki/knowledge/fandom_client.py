# src/wiki/knowledge/fandom_client.py
# GROUP: wiki
# DESCRIPTION: Clean Fandom wiki extractor (Tiles Survive safe context layer)

import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger("wiki.fandom")

BASE_URL = "https://tiles-survive.fandom.com/wiki/"


def _clean_text(html: str) -> str:
    """
    Extracts readable article text from Fandom HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    # remove junk
    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()

    content = soup.find("div", {"class": "mw-parser-output"})

    if not content:
        return ""

    paragraphs = content.find_all("p")

    text_parts = []

    for p in paragraphs:
        txt = p.get_text(strip=True)
        if len(txt) > 40:  # filter noise
            text_parts.append(txt)

    return "\n".join(text_parts[:15])  # limit context size


async def fetch_fandom_page(query: str) -> str:
    """
    Fetch and clean Fandom wiki page content.
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

        cleaned = _clean_text(html)

        if not cleaned:
            logger.warning("Empty Fandom extraction for: %s", query)
            return ""

        logger.info("Fandom extracted chars: %s", len(cleaned))

        return cleaned

    except Exception as e:
        logger.exception("Fandom fetch failed: %s", e)
        return ""