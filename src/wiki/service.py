# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Gemini (prompt-engineered knowledge layer)

import logging

from src.ai.gemini import gemini_client

logger = logging.getLogger("wiki.service")


# =========================
# PROMPT ENGINE
# =========================

def build_wiki_prompt(user_text: str) -> str:
    """
    Converts user query into Wikipedia-style AI prompt.
    """

    return f"""
You are an AI Wikipedia-style assistant.

Rules:
- Answer like Wikipedia (neutral, factual, structured)
- If you are unsure, say you are not certain
- Keep answers concise but informative
- Do not hallucinate facts

User question:
{user_text}

Answer:
""".strip()


# =========================
# MAIN SERVICE
# =========================

async def answer_wiki_question(text: str) -> str:
    """
    Main entry point for AI wiki responses.
    """

    logger.info("Wiki query received: %s", text)

    if not text or not text.strip():
        return "Please provide a valid question."

    prompt = build_wiki_prompt(text)

    try:
        response = await gemini_client.generate(prompt)

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")

        return "⚠️ AI service error. Please try again later."