# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Gemini (Tiles Survive domain-locked assistant)

import logging

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


# =========================
# PROMPT ENGINE
# =========================

def build_wiki_prompt(user_text: str) -> str:
    """
    Strict domain prompt for Gemini (game-only context).
    """

    return f"""
You are an expert wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

CRITICAL RULES:
- Answer ONLY about "{GAME_NAME}"
- Do NOT use outside knowledge
- If unsure, say "I am not sure"
- Do NOT hallucinate game mechanics

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
    Main AI entrypoint (guarded + domain restricted).
    """

    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    # =========================
    # 🧠 GUARD LAYER (NEW)
    # =========================
    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # 🤖 GEMINI LAYER
    # =========================
    prompt = build_wiki_prompt(text)

    try:
        response = await gemini_client.generate(prompt)

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."