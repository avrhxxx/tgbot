# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v8 (Wikipedia + SearXNG)

import logging
import os

from src.wiki.knowledge.wikipedia_client import fetch_wikipedia
from src.wiki.knowledge.searx_client import SearxClient

logger = logging.getLogger("wiki.aggregator")

searx = SearxClient(
    base_url=os.getenv("SEARX_URL", "https://searx.be")
)


def _dedup(items: list[str]) -> list[str]:
    seen = set()
    out = []

    for item in items:
        clean = item.strip()
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)

    return out


def _tag_block(tag: str, title: str, items: list[str]) -> str:
    if not items:
        return ""

    lines = [f"[{tag}] {title}"]

    for item in items[:5]:
        lines.append(f"- {item}")

    return "\n".join(lines)


async def build_knowledge_context(query: str) -> str:

    logger.info("Building knowledge context for: %s", query)

    # =========================
    # SOURCES
    # =========================
    wiki_raw = await fetch_wikipedia(query)
    web_raw = await searx.search(query)

    wiki = _dedup(wiki_raw)
    web = _dedup(web_raw)

    parts = []

    # =========================
    # FACTS
    # =========================
    if wiki:
        parts.append(
            _tag_block("FACT", "WIKIPEDIA", wiki)
        )

    # =========================
    # WEB SEARCH (SEARXNG)
    # =========================
    if web:
        parts.append(
            _tag_block("WEB", "SEARX SEARCH RESULTS", web)
        )

    # =========================
    # FALLBACK
    # =========================
    if not parts:
        parts.append(
            "[SYSTEM]\n"
            "- No reliable sources found\n"
            "- Do not guess\n"
            "- Respond: I am not sure based on available sources"
        )

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final