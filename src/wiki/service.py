# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service (RAG v2 + session-aware context)

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.ai.prompt_engine import build_prompt

from src.wiki.embeddings.vector_store import VectorStore
from src.wiki.embeddings.client import EmbeddingClient
from src.wiki.knowledge.firestore_client import FirestoreClient

from src.services.session_service import (
    update_session,
    build_session_context,
)

logger = logging.getLogger("wiki.service")

firestore = FirestoreClient()
embedder = EmbeddingClient()
vector_store = VectorStore(firestore, embedder)


async def answer_wiki_question(text: str, user_id: int | None = None) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # SESSION CONTEXT (NEW)
    # =========================
    session_context = ""

    if user_id is not None:
        session_context = build_session_context(user_id)

    # =========================
    # VECTOR SEARCH
    # =========================
    try:
        results = await vector_store.search(text, limit=5)
    except Exception:
        logger.exception("Vector search failed")
        results = []

    context_parts = []

    entities = []
    topic = None

    for r in results:
        content = r.get("content", "")
        url = r.get("url", "")
        topic = r.get("topic", topic)

        if not content:
            continue

        context_parts.append(
            f"[TOPIC: {topic}]\nSOURCE: {url}\n{content}"
        )

        if topic:
            entities.append(topic)

    context = "\n\n---\n\n".join(context_parts).strip()

    if not context:
        context = "[NO RELEVANT MEMORY FOUND]"

    # =========================
    # PROMPT BUILD
    # =========================
    final_context = context

    if session_context:
        final_context = session_context + "\n\n" + context

    prompt = build_prompt(text, final_context)

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

    finally:
        # =========================
        # SESSION UPDATE (POST)
        # =========================
        if user_id is not None:
            update_session(
                user_id,
                topic=topic,
                entities=entities,
                question=text,
            )