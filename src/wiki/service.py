# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Gemini (Tiles Survive domain-locked assistant)

import logging

from src.ai.gemini import gemini_client

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"


# =========================
# PROMPT ENGINE
# =========================

def build_wiki_prompt(user_text: str) -> str:
    """
    Strict domain prompt - AI is ONLY allowed to answer about Tiles Survive!
    """

    return f"""
You are an expert wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

CRITICAL RULES:
- You ONLY answer questions about "{GAME_NAME}"
- If the question is NOT about this game, respond EXACTLY:
  "I can only answer questions about Tiles Survive!."
- Do NOT use general knowledge outside the game
- Do NOT invent mechanics or items
- If unsure about something in-game, say "I am not sure"

Style rules:
- Wikipedia-like tone
- structured answers
- clear sections if needed
- practical tips when relevant

User question:
{user_text}

Answer:
""".strip()


# =========================
# MAIN SERVICE
# =========================

async def answer_wiki_question(text: str) -> str:
    """
    Main AI entrypoint (game-restricted).
    """

    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    prompt = build_wiki_prompt(text)

    try:
        response = await gemini_client.generate(prompt)

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")

        return "⚠️ AI service error. Please try again later."