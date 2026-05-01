# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v5 (Wikipedia + DDG only, improved reliability)

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


def _is_low_quality(wiki: list[str], ddg: list[str]) -> bool:
    """
    Detects weak context signal (important for prompt behavior)
    """
    return len(wiki) == 0 and len(ddg) == 0


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
    # WIKIPEDIA
    # =========================
    if wiki:
        parts.append(_format_block("WIKIPEDIA (HIGH TRUST)", wiki))

    # =========================
    # DDG
    # =========================
    if ddg:
        parts.append(_format_block("WEB SEARCH (DUCKDUCKGO)", ddg))

    # =========================
    # CRITICAL SIGNAL FOR AI
    # =========================
    if _is_low_quality(wiki, ddg):
        parts.append(
            "[SYSTEM NOTE]\n"
            "- No reliable sources found in Wikipedia or web search\n"
            "- Answer ONLY if you are confident from general knowledge\n"
            "- Otherwise say: I am not sure based on available sources"
        )

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final