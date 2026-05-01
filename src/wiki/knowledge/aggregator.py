# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: Weighted knowledge aggregator v2 (Reddit + Fandom + Search → normalized AI context)

import logging

from src.wiki.knowledge.reddit_client import search_reddit
from src.wiki.knowledge.fandom_client import fetch_fandom_page
from src.wiki.knowledge.google_client import google_search

logger = logging.getLogger("wiki.aggregator")


# =========================
# HELPERS
# =========================

def _dedup(items: list[str]) -> list[str]:
    """
    Removes duplicate strings while preserving order.
    """
    seen = set()
    out = []

    for item in items:
        clean = item.strip()
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)

    return out


def _split_fandom(text: str) -> list[str]:
    """
    Converts raw fandom text into structured lines.
    """
    if not text:
        return []

    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 40]
    return lines


def _format_block(title: str, items: list[str], max_items: int = 5) -> str:
    """
    Clean formatting + safe truncation for LLM context.
    """
    if not items:
        return ""

    trimmed = items[:max_items]

    lines = [f"[{title}]"]

    for item in trimmed:
        lines.append(f"- {item}")

    return "\n".join(lines)


# =========================
# MAIN AGGREGATOR
# =========================

async def build_knowledge_context(query: str) -> str:
    """
    Builds normalized, structured context for Gemini RAG.
    """

    logger.info("Building knowledge context for: %s", query)

    # =========================
    # FETCH SOURCES
    # =========================
    reddit_raw = await search_reddit(query)
    fandom_raw = await fetch_fandom_page(query)
    search_raw = await google_search(query)

    # =========================
    # NORMALIZATION
    # =========================
    reddit_data = _dedup(reddit_raw)
    fandom_data = _dedup(_split_fandom(fandom_raw))
    search_data = _dedup(search_raw)

    parts = []

    # =========================
    # FANDOM (HIGH TRUST)
    # =========================
    if fandom_data:
        parts.append(
            _format_block("FANDOM WIKI (HIGH TRUST)", fandom_data, max_items=5)
        )

    # =========================
    # REDDIT (COMMUNITY SIGNAL)
    # =========================
    if reddit_data:
        parts.append(
            _format_block("REDDIT COMMUNITY INSIGHTS", reddit_data, max_items=5)
        )

    # =========================
    # SEARCH (LOWER TRUST)
    # =========================
    if search_data:
        parts.append(
            _format_block("WEB SEARCH SNIPPETS (LOW TRUST)", search_data, max_items=5)
        )

    final_context = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final_context))

    return final_context