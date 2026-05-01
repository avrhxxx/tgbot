# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Gemini (Tiles Survive context-grounded assistant)

import logging

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.search import fetch_reddit_context

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


# =========================
# PROMPT ENGINE
# =========================

def build_wiki_prompt(user_text: str, context: str) -> str:
    """
    Context-grounded prompt (prevents hallucinations).
    """

    return f"""
You are an expert wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

You MUST use ONLY the provided context below.
Do NOT invent information outside it.

========================
CONTEXT (from community / Reddit / guides):
{context}
========================

CRITICAL RULES:
- Answer ONLY about "{GAME_NAME}"
- If context does not contain answer, say: "I am not sure based on available data"
- Do NOT hallucinate
- Be concise and structured

Style:
- Wikipedia-like sections
- practical gameplay advice
- clear bullet points when useful

User question:
{user_text}

Answer:
""".strip()


# =========================
# MAIN SERVICE
# =========================

async def answer_wiki_question(text: str) -> str:
    """
    Main AI entrypoint (guarded + context-based reasoning).
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
    # 🌐 WEB CONTEXT LAYER (Reddit mock)
    # =========================
    context = fetch_reddit_context(text)

    # =========================
    # 🤖 GEMINI LAYER (grounded)
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