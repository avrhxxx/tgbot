# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: RAG aggregator v7 (Wikipedia + DDG + page fetch with trust hierarchy)

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


def _tag_block(tag: str, title: str, items: list[str]) -> str:
    if not items:
        return ""

    lines = [f"[{tag}] {title}"]

    for item in items[:5]:
        lines.append(f"- {item}")

    return "\n".join(lines)


# =========================
# HTML EXTRACTOR
# =========================

def _extract_text(html: str) -> str:
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
# FETCH PAGE
# =========================

async def _fetch_page(url: str) -> str:
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
    # FACTS (WIKI - HIGHEST TRUST)
    # =========================
    if wiki:
        parts.append(
            _tag_block("FACT", "WIKIPEDIA", wiki)
        )

    # =========================
    # META + WEB
    # =========================
    if ddg:
        parts.append(
            _tag_block("META", "WEB SNIPPETS", ddg)
        )

        urls = []
        for item in ddg:
            if "http" in item:
                for p in item.split():
                    if p.startswith("http"):
                        urls.append(p)

        urls = urls[:3]

        for url in urls:
            page_text = await _fetch_page(url)

            if page_text:
                parts.append(
                    _tag_block("RAW", "SOURCE PAGE", [page_text])
                )

    # =========================
    # STRONG FALLBACK SIGNAL
    # =========================
    if not parts:
        parts.append(
            "[SYSTEM RULE]\n"
            "- No reliable sources found\n"
            "- Do NOT guess\n"
            "- If unsure: say 'I am not sure based on available sources'"
        )

    final = "\n\n".join(parts).strip()

    logger.info("Context built length: %s", len(final))

    return final