# src/wiki/knowledge/aggregator.py
# GROUP: wiki
# DESCRIPTION: Firestore-only knowledge context builder (RAG layer)

import logging
from typing import List, Dict, Any

from src.wiki.knowledge.firestore_client import FirestoreClient

logger = logging.getLogger("wiki.aggregator")

firestore = FirestoreClient()


def _format_block(items: List[str]) -> str:
    if not items:
        return ""
    return "\n".join(f"- {i}" for i in items)


async def build_knowledge_context(query: str) -> str:
    logger.info("Firestore-only context for: %s", query)

    try:
        # FIX: correct method name (v2 API)
        docs: List[Dict[str, Any]] = await firestore.search_knowledge_raw()

        if not docs:
            return "[NO DATA]\nNo stored knowledge found."

        parts: List[str] = []

        for d in docs:
            if not isinstance(d, dict):
                continue

            topic = str(d.get("topic", "") or "")
            content = str(d.get("content", "") or "")
            url = str(d.get("url", "") or "")

            if not content:
                continue

            block = f"[TOPIC: {topic}]"
            if url:
                block += f"\nSOURCE: {url}"

            block += f"\n{content[:1500]}"

            parts.append(block)

        if not parts:
            return "[NO DATA]\nNo usable knowledge found."

        return "\n\n---\n\n".join(parts)

    except Exception as e:
        logger.exception("Firestore read failed: %s", e)
        return "[ERROR] Unable to fetch knowledge"