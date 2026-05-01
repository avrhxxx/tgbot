# src/wiki/knowledge/tavily_client.py
# GROUP: wiki
# DESCRIPTION: Tavily AI web search client (RAG-grade source, replaces DDG scraping)

import os
import logging
import aiohttp
from aiohttp import ClientTimeout

logger = logging.getLogger("wiki.tavily")

TAVILY_URL = "https://api.tavily.com/search"


def _extract_results(data: dict) -> list[str]:
    """
    Normalizes Tavily response into clean text snippets for RAG.
    """
    results = []

    items = data.get("results", [])
    if not isinstance(items, list):
        return []

    for item in items:
        title = item.get("title", "")
        content = item.get("content", "")
        url = item.get("url", "")

        if not content and not title:
            continue

        snippet = f"{title} - {content}".strip()

        if url:
            snippet += f" ({url})"

        if len(snippet) > 60:
            results.append(snippet[:800])

    return results[:7]


async def search_tavily(query: str) -> list[str]:
    """
    Performs web search using Tavily API (optimized for LLM/RAG).
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        logger.warning("TAVILY_API_KEY missing")
        return []

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_raw_content": False,
        "max_results": 5,
    }

    headers = {
        "Content-Type": "application/json"
    }

    timeout = ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                TAVILY_URL,
                json=payload,
                headers=headers,
                timeout=timeout
            ) as resp:

                if resp.status != 200:
                    logger.warning("Tavily HTTP error: %s", resp.status)
                    return []

                data = await resp.json()

        results = _extract_results(data)

        logger.info("Tavily results: %s", len(results))

        return results

    except Exception as e:
        logger.exception("Tavily search failed: %s", e)
        return []