# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Vertex AI RAG assistant

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.aggregator import build_knowledge_context

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


def build_wiki_prompt(user_text: str, context: str) -> str:
    return f"""
You are a STRICT factual wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

========================
STRICT MODE RULES
========================
1. You can ONLY use the CONTEXT below
2. If context is empty or weak → say EXACTLY:
   "I am not sure based on available sources."
3. Never guess or use general knowledge
4. Never hallucinate game mechanics
5. If unsure → say you don't know

========================
CONTEXT
========================
{context}
========================

USER QUESTION:
{user_text}

ANSWER (be precise, factual only):
""".strip()


def _extract_sources(context: str) -> str:
    sources = []

    if "WIKIPEDIA" in context:
        sources.append("Wikipedia")

    if "DUCKDUCKGO" in context:
        sources.append("Web Search (DDG)")

    if "[SYSTEM NOTE]" in context:
        sources.append("System Constraint Layer")

    return "Sources: " + ", ".join(sources) if sources else "Sources: None"


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    context = await build_knowledge_context(text)

    sources = _extract_sources(context)

    prompt = build_wiki_prompt(text, context)

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