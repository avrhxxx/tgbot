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

    if not html:
        return ""

    # try to isolate main content block (Fandom structure-aware)
    start_marker = 'mw-parser-output'
    if start_marker not in html:
        return ""

    # crude but effective extraction window
    parts = html.split("<p>")

    text_blocks = []

    for part in parts:
        # stop junk sections
        if "</p>" in part:
            clean = part.split("</p>")[0]

            # remove leftover tags
            clean = clean.replace("<b>", "").replace("</b>", "")
            clean = clean.replace("<i>", "").replace("</i>", "")
            clean = clean.replace("<br>", "\n")

            clean = clean.strip()

            if len(clean) > 40:
                text_blocks.append(clean)

    return "\n".join(text_blocks[:15])


async def fetch_fandom_page(query: str) -> str:
    """
    Fetch and clean Fandom wiki page content.
    """

    page_name = query.strip().replace(" ", "_")
    url = f"{BASE_URL}{page_name}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:

                # 🔴 FIX: avoid false positives (404 / redirect pages)
                if resp.status != 200:
                    logger.warning("Fandom HTTP error: %s", resp.status)
                    return ""

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