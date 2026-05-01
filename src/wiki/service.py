# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Vertex AI RAG assistant

import logging

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.aggregator import build_knowledge_context

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


def build_wiki_prompt(user_text: str, context: str) -> str:
    return f"""
You are an expert wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

You MUST answer ONLY using the provided CONTEXT.
If information is missing in context, say:
"I am not sure based on available sources."

========================
CONTEXT (REDDIT + FANDOM + SEARCH)
========================
{context}
========================

CRITICAL RULES:
- Do NOT invent mechanics or items
- Do NOT use outside knowledge
- Be strictly factual

User question:
{user_text}

Answer:
""".strip()


def _extract_sources(context: str) -> str:
    sources = []

    if "[FANDOM WIKI" in context:
        sources.append("Fandom Wiki")

    if "[REDDIT" in context:
        sources.append("Reddit Community")

    if "[WEB SEARCH" in context:
        sources.append("Web Search")

    return "Sources: " + ", ".join(sources) if sources else "Sources: None"


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    context = await build_knowledge_context(text)

    if not context or len(context.strip()) < 20:
        context = "No reliable external sources found."

    sources = _extract_sources(context)

    prompt = build_wiki_prompt(text, context)

    try:
        response = gemini_client.generate(prompt)

        if not response:
            return "No response from AI."

        return f"{response.strip()}\n\n---\n{sources}"

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."