# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: Weighted knowledge aggregator (Reddit + Fandom + Search → structured AI context)

import logging

from src.wiki.knowledge.reddit_client import search_reddit
from src.wiki.knowledge.fandom_client import fetch_fandom_page
from src.wiki.knowledge.google_client import google_search

logger = logging.getLogger("wiki.aggregator")

# =========================
# WEIGHT CONFIG
# =========================

WEIGHTS = {
    "fandom": 3,
    "reddit": 2,
    "search": 1
}


def _format_block(title: str, items: list[str], max_items: int = 5) -> str:
    """
    Clean formatting + limit enforcement.
    """

    if not items:
        return ""

    trimmed = items[:max_items]

    lines = [f"[{title}]"]

    for i in trimmed:
        clean = i.strip()
        if clean:
            lines.append(f"- {clean}")

    return "\n".join(lines)


# =========================
# MAIN AGGREGATOR
# =========================

async def build_knowledge_context(query: str) -> str:
    """
    Builds weighted, structured context for Gemini.
    """

    logger.info("Building knowledge context for: %s", query)

    reddit_data = await search_reddit(query)
    fandom_data = await fetch_fandom_page(query)
    search_data = await google_search(query)

    parts = []

    # =========================
    # FANDOM (HIGH TRUST)
    # =========================
    if fandom_data:
        parts.append(
            _format_block("FANDOM WIKI (HIGH TRUST)", [fandom_data], max_items=1)
        )

    # =========================
    # REDDIT (COMMUNITY)
    # =========================
    if reddit_data:
        parts.append(
            _format_block("REDDIT COMMUNITY INSIGHTS", reddit_data, max_items=5)
        )

    # =========================
    # SEARCH (UNCERTAIN)
    # =========================
    if search_data:
        parts.append(
            _format_block("WEB SEARCH SNIPPETS (LOWER TRUST)", search_data, max_items=5)
        )

    final_context = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final_context))

    return final_context