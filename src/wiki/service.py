# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Firestore + Prompt Engine + Gemini

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.ai.prompt_engine import build_prompt

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"

firestore = FirestoreClient()


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # FIRESTORE CONTEXT
    # =========================
    try:
        docs = await firestore.search_knowledge(text)
    except Exception:
        logger.exception("Firestore query failed")
        docs = []

    context_parts = []

    if docs:
        for d in docs:
            topic = d.get("topic", "")
            content = d.get("content", "")
            url = d.get("url", "")

            if not content:
                continue

            # 🔥 SOURCE ADDED (important for RAG trust)
            context_parts.append(
                f"[TOPIC: {topic}]\nSOURCE: {url}\n{content[:1500]}"
            )

    context = "\n\n---\n\n".join(context_parts).strip()

    if not context:
        context = "[NO SOURCES FOUND]"

    # =========================
    # PROMPT ENGINE
    # =========================
    prompt = build_prompt(text, context)

    # =========================
    # GEMINI CALL
    # =========================
    try:
        response = await asyncio.to_thread(
            gemini_client.generate,
            prompt
        )

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."