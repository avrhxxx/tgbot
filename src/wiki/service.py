# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service (RAG v2 - vector + fallback hybrid + sources footer)

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.ai.prompt_engine import build_prompt

from src.wiki.embeddings.client import EmbeddingClient
from src.wiki.embeddings.vector_store import VectorStore

logger = logging.getLogger("wiki.service")

# =========================
# INIT LAYERS
# =========================
firestore = FirestoreClient()
embedder = EmbeddingClient()
vector_store = VectorStore(firestore, embedder)


# =========================
# SOURCES FORMATTER (FOOTER)
# =========================
def format_sources_footer(sources: list[dict]) -> str:
    if not sources:
        return ""

    lines = ["\n──────────────", "📚 Sources:"]

    for s in sources[:5]:
        topic = s.get("topic", "unknown")
        url = s.get("url", "")
        created_at = s.get("created_at", "")

        if created_at:
            lines.append(f"• {topic} – {created_at}")
        else:
            lines.append(f"• {topic}")

    return "\n".join(lines)


# =========================
# MAIN SERVICE
# =========================
async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    # =========================
    # SOFT GUARD (NO BLOCKING)
    # =========================
    if not is_game_related(text):
        logger.info("Non-game query detected, still processing via RAG fallback")

    # =========================
    # VECTOR RETRIEVAL (RAG v2)
    # =========================
    try:
        results = await vector_store.search(text, limit=5)
    except Exception:
        logger.exception("Vector search failed")
        results = []

    context_parts: list[str] = []
    sources: list[dict] = []

    # =========================
    # BUILD CONTEXT + SOURCES
    # =========================
    for r in results:
        content = r.get("content", "")
        url = r.get("url", "")
        topic = r.get("topic", "")
        created_at = r.get("created_at", None)

        if not content:
            continue

        context_parts.append(
            f"[TOPIC: {topic}]\nSOURCE: {url}\n{content}"
        )

        sources.append({
            "topic": topic,
            "url": url,
            "created_at": created_at
        })

    context = "\n\n---\n\n".join(context_parts).strip()

    if not context:
        context = "[NO RELEVANT MEMORY FOUND]"

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

        final = response.strip()
        final += format_sources_footer(sources)

        return final

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."