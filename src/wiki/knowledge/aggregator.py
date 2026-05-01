# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: Knowledge aggregator (Reddit + Fandom + Google → unified context)

import logging

from src.wiki.knowledge.reddit_client import search_reddit
from src.wiki.knowledge.fandom_client import fetch_fandom_page
from src.wiki.knowledge.google_client import google_search

logger = logging.getLogger("wiki.aggregator")


async def build_knowledge_context(query: str) -> str:
    """
    Combines multiple sources into a single clean context for Gemini.
    """

    logger.info("Building knowledge context for: %s", query)

    reddit_data = await search_reddit(query)
    fandom_data = await fetch_fandom_page(query)
    google_data = await google_search(query)

    context_parts = []

    if reddit_data:
        context_parts.append("=== REDDIT ===")
        context_parts.extend(reddit_data)

    if fandom_data:
        context_parts.append("=== FANDOM WIKI ===")
        context_parts.append(fandom_data)

    if google_data:
        context_parts.append("=== GOOGLE SNIPPETS ===")
        context_parts.extend(google_data)

    final_context = "\n\n".join(context_parts)

    logger.info("Context built length: %s", len(final_context))

    return final_context