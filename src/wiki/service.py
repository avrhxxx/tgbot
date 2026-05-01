# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Gemini (Tiles Survive real internet RAG assistant)

import logging

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.aggregator import build_knowledge_context

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


# =========================
# PROMPT ENGINE
# =========================

def build_wiki_prompt(user_text: str, context: str) -> str:
    """
    Context-grounded prompt (anti-hallucination RAG mode).
    """

    return f"""
You are an expert wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

You MUST answer ONLY using the provided CONTEXT.
If information is missing in context, explicitly say:
"I am not sure based on available sources."

========================
CONTEXT (REAL SOURCES: Reddit + Fandom + Google)
{context}
========================

CRITICAL RULES:
- Answer ONLY about "{GAME_NAME}"
- Do NOT invent mechanics or items
- Do NOT use outside knowledge
- Be strict and factual
- Prefer bullet points when helpful

Style:
- Wikipedia-like structure
- clear sections
- practical gameplay advice

User question:
{user_text}

Answer:
""".strip()


# =========================
# MAIN SERVICE
# =========================

async def answer_wiki_question(text: str) -> str:
    """
    Main AI entrypoint (FULL RAG: Reddit + Fandom + Google).
    """

    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    # =========================
    # 🧠 GUARD LAYER
    # =========================
    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # 🌐 REAL INTERNET KNOWLEDGE LAYER
    # =========================
    context = await build_knowledge_context(text)

    if not context:
        context = "No external sources found."

    # =========================
    # 🤖 GEMINI LAYER (context-only)
    # =========================
    prompt = build_wiki_prompt(text, context)

    try:
        response = await gemini_client.generate(prompt)

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."