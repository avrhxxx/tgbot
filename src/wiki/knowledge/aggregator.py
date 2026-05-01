# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v6 (Wikipedia + DDG + page fetch)

import logging
import aiohttp
from aiohttp import ClientTimeout

from src.wiki.knowledge.wikipedia_client import fetch_wikipedia
from src.wiki.knowledge.ddg_client import search_ddg

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


def _format_block(title: str, items: list[str]) -> str:
    if not items:
        return ""

    lines = [f"[{title}]"]

    for item in items[:5]:
        lines.append(f"- {item}")

    return "\n".join(lines)


# =========================
# SIMPLE HTML EXTRACTOR
# =========================

def _extract_text(html: str) -> str:
    """
    Very lightweight text extraction (CI-safe, no deps).
    """
    if not html:
        return ""

    text = (
        html.replace("<script", " ")
            .replace("<style", " ")
            .replace("<", " ")
            .replace(">", " ")
    )

    text = " ".join(text.split())

    return text[:1500]


# =========================
# FETCH PAGE CONTENT
# =========================

async def _fetch_page(url: str) -> str:
    """
    Fetches raw HTML from a page.
    """
    try:
        headers = {
            "User-Agent": "shadow-wiki-bot/1.0"
        }

        timeout = ClientTimeout(total=10)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=headers,
                timeout=timeout
            ) as resp:

                if resp.status != 200:
                    return ""

                html = await resp.text()
                return _extract_text(html)

    except Exception as e:
        logger.warning("Page fetch failed: %s", e)
        return ""


# =========================
# MAIN
# =========================

async def build_knowledge_context(query: str) -> str:

    logger.info("Building knowledge context for: %s", query)

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
    # DDG (SNIPPETS)
    # =========================
    if ddg:
        parts.append(_format_block("WEB SEARCH (SNIPPETS)", ddg))

        # =========================
        # PAGE FETCH (NEW 🔥)
        # =========================
        urls = []
        for item in ddg:
            if "http" in item:
                parts_split = item.split()
                for p in parts_split:
                    if p.startswith("http"):
                        urls.append(p)

        urls = urls[:3]

        for url in urls:
            page_text = await _fetch_page(url)

            if page_text:
                parts.append(
                    _format_block("SOURCE PAGE", [page_text])
                )

    # =========================
    # FALLBACK SIGNAL
    # =========================
    if not parts:
        parts.append(
            "[SYSTEM NOTE]\n"
            "- No sources found\n"
            "- Answer ONLY if confident\n"
            "- Otherwise say: I am not sure based on available sources"
        )

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final