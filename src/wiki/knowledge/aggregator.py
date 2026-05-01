# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: Knowledge aggregator v3 (Google Search only → clean RAG context)

import logging

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
    Builds normalized context using Google Search only.
    """

    logger.info("Building knowledge context for: %s", query)

    # =========================
    # FETCH (ONLY GOOGLE)
    # =========================
    search_raw = await google_search(query)

    # =========================
    # NORMALIZATION
    # =========================
    search_data = _dedup(search_raw)

    parts = []

    # =========================
    # SEARCH (PRIMARY SOURCE)
    # =========================
    if search_data:
        parts.append(
            _format_block(
                "WEB SEARCH (GOOGLE - PRIMARY SOURCE)",
                search_data,
                max_items=5,
            )
        )

    final_context = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final_context))

    return final_context