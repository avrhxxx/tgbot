# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Vertex AI RAG assistant

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.aggregator import build_knowledge_context
from src.wiki.knowledge.firestore_client import FirestoreClient

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"

firestore = FirestoreClient()


def build_wiki_prompt(user_text: str, context: str) -> str:
    return f"""
You are a knowledgeable wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

========================
INSTRUCTIONS
========================
- PRIORITIZE facts from USER PROVIDED DATA if present
- Base your answer on the CONTEXT below
- You may summarize and combine multiple sources
- Be careful and factual

If there is no useful information, say EXACTLY:
"I am not sure based on available sources."

========================
CONTEXT
========================
{context}
========================

RULES:
- Do NOT invent mechanics
- Do NOT hallucinate features
- Prefer "I am not sure" over guessing

USER QUESTION:
{user_text}

ANSWER:
""".strip()


def _extract_sources(context: str) -> str:
    sources = []

    if "[USER DATA]" in context:
        sources.append("User Knowledge Base")

    if "WIKIPEDIA" in context:
        sources.append("Wikipedia")

    if "SEARX" in context:
        sources.append("Web Search")

    if "[NO SOURCES FOUND]" in context:
        sources.append("No sources")

    return "Sources: " + ", ".join(sources) if sources else "Sources: None"


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # 🔥 1. FIRESTORE FIRST
    # =========================
    user_data = await firestore.search_knowledge(text)

    parts = []

    if user_data:
        parts.append("[USER DATA]")
        for item in user_data:
            parts.append(f"- {item[:1000]}")

    # =========================
    # 🔥 2. FALLBACK (WEB)
    # =========================
    if not user_data:
        context = await build_knowledge_context(text)

        if context:
            parts.append(context)

    # =========================
    # FINAL CONTEXT
    # =========================
    final_context = "\n\n".join(parts).strip()

    if not final_context:
        final_context = "[NO SOURCES FOUND]"

    sources = _extract_sources(final_context)

    prompt = build_wiki_prompt(text, final_context)

    try:
        response = await asyncio.to_thread(
            gemini_client.generate,
            prompt
        )

        if not response:
            return "No response from AI."

        return f"{response.strip()}\n\n---\n{sources}"

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."