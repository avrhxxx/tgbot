# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: MVP wiki service (placeholder for Gemini AI layer)

import logging

logger = logging.getLogger("wiki.service")


async def answer_wiki_question(text: str) -> str:
    """
    Temporary stub for AI wiki responses.
    Will be replaced by Gemini-powered logic.
    """

    logger.info("Wiki query received: %s", text)

    return f"🧠 Wiki (MVP): I received your question -> {text}"