# src/wiki/knowledge/fandom_client.py
# GROUP: wiki
# DESCRIPTION: Clean Fandom wiki extractor (Tiles Survive safe context layer)

import logging
import aiohttp

logger = logging.getLogger("wiki.fandom")

BASE_URL = "https://tiles-survive.fandom.com/wiki/"


def _clean_text(html: str) -> str:
    """
    Lightweight HTML extraction (MVP-safe, no external parser).
    """

    # naive fallback extraction (CI-safe, no bs4 dependency)

    # remove scripts/styles quickly
    cleaned = html.replace("<script", " <script").replace("<style", " <style")

    # very rough text slicing fallback
    # (you can replace later with BS4 or lxml parser layer)
    text = cleaned

    # extract only paragraph-like chunks
    parts = []

    for chunk in text.split("</p>"):
        if "<p" in chunk:
            inner = chunk.split("<p")[-1]
            inner = inner.split(">")[-1].strip()

            if len(inner) > 40:
                parts.append(inner)

    return "\n".join(parts[:15])


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