# GROUP: wiki
# DESCRIPTION: Firestore-only knowledge context builder

import logging

from src.wiki.knowledge.firestore_client import FirestoreClient

logger = logging.getLogger("wiki.aggregator")

firestore = FirestoreClient()


def _format_block(items):
    if not items:
        return ""
    return "\n".join([f"- {i}" for i in items])


async def build_knowledge_context(query: str) -> str:
    logger.info("Firestore-only context for: %s", query)

    try:
        docs = await firestore.search_knowledge(query)

        if not docs:
            return "[NO DATA]\nNo stored knowledge found."

        parts = []

        for d in docs:
            topic = d.get("topic", "")
            content = d.get("content", "")

            if not content:
                continue

            parts.append(
                f"[TOPIC: {topic}]\n{content[:1500]}"
            )

        return "\n\n---\n\n".join(parts)

    except Exception as e:
        logger.exception("Firestore read failed: %s", e)
        return "[ERROR] Unable to fetch knowledge"