# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v8 (Wikipedia + Tavily, clean AI-grade search)

import logging

from src.wiki.knowledge.wikipedia_client import fetch_wikipedia
from src.wiki.knowledge.tavily_client import search_tavily

logger = logging.getLogger("wiki.aggregator")


# =========================
# HELPERS
# =========================

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


# =========================
# MAIN
# =========================

async def build_knowledge_context(query: str) -> str:

    logger.info("Building knowledge context for: %s", query)

    # =========================
    # SOURCES
    # =========================
    wiki_raw = await fetch_wikipedia(query)
    web_raw = await search_tavily(query)

    wiki = _dedup(wiki_raw)
    web = _dedup(web_raw)

    parts = []

    # =========================
    # FACTS (WIKIPEDIA)
    # =========================
    if wiki:
        parts.append(
            _tag_block("FACT", "WIKIPEDIA", wiki)
        )

    # =========================
    # WEB (TAVILY - AI SEARCH)
    # =========================
    if web:
        parts.append(
            _tag_block("WEB", "TAVILY SEARCH RESULTS", web)
        )

    # =========================
    # HARD FALLBACK SIGNAL
    # =========================
    if not parts:
        parts.append(
            "[SYSTEM RULE]\n"
            "- No reliable sources found\n"
            "- Do NOT guess or hallucinate\n"
            "- Respond: I am not sure based on available sources"
        )

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final