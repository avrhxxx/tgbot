# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v5 (Wikipedia + DDG only, no paid APIs)

import logging

from src.wiki.knowledge.wikipedia_client import fetch_wikipedia
from src.wiki.knowledge.ddg_client import search_ddg

logger = logging.getLogger("wiki.aggregator")


def _dedup(items: list[str]) -> list[str]:
    seen = set()
    out = []

    for item in items:
        clean = item.strip()
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)

    return out


def _format_block(title: str, items: list[str]) -> str:
    if not items:
        return ""

    lines = [f"[{title}]"]

    for item in items[:5]:
        lines.append(f"- {item}")

    return "\n".join(lines)


async def build_knowledge_context(query: str) -> str:

    logger.info("Building knowledge context for: %s", query)

    # =========================
    # SOURCES
    # =========================
    wiki_raw = await fetch_wikipedia(query)
    ddg_raw = await search_ddg(query)

    wiki = _dedup(wiki_raw)
    ddg = _dedup(ddg_raw)

    parts = []

    # =========================
    # WIKIPEDIA (HIGH TRUST)
    # =========================
    if wiki:
        parts.append(_format_block("WIKIPEDIA (HIGH TRUST)", wiki))

    # =========================
    # DDG (WEB SIGNAL)
    # =========================
    if ddg:
        parts.append(_format_block("WEB SEARCH (DUCKDUCKGO)", ddg))

    if not parts:
        parts.append("[NO SOURCES FOUND]")

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final