# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service powered by Vertex AI + Firestore-only RAG

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.firestore_client import FirestoreClient

logger = logging.getLogger("wiki.service")

GAME_NAME = "Tiles Survive!"
GAME_RULE = "mobile game by FunPlus International"

firestore = FirestoreClient()


# =========================
# PROMPT BUILDER
# =========================
def build_wiki_prompt(user_text: str, context: str) -> str:
    return f"""
You are a knowledgeable wiki assistant for the mobile game "{GAME_NAME}" ({GAME_RULE}).

========================
INSTRUCTIONS
========================
- Use ONLY the provided CONTEXT
- CONTEXT comes from a user-maintained knowledge base (Firestore)
- If context is insufficient, say EXACTLY:
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


# =========================
# SOURCES LABEL
# =========================
def _extract_sources(has_data: bool) -> str:
    return "Sources: Firestore Knowledge Base" if has_data else "Sources: None"


# =========================
# MAIN ENTRY
# =========================
async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # FIRESTORE ONLY RETRIEVAL
    # =========================
    try:
        docs = await firestore.search_knowledge(text)
    except Exception:
        logger.exception("Firestore query failed")
        docs = []

    # =========================
    # BUILD CONTEXT
    # =========================
    context_parts = []

    # 🔥 FIX: docs is List[str], NOT dict
    if docs:
        for content in docs:
            if not content:
                continue

            context_parts.append(
                f"[USER KNOWLEDGE]\n{content[:1500]}"
            )

    final_context = "\n\n---\n\n".join(context_parts).strip()

    has_data = bool(final_context)

    if not has_data:
        final_context = "[NO SOURCES FOUND]"

    # =========================
    # GEMINI PROMPT
    # =========================
    prompt = build_wiki_prompt(text, final_context)

    try:
        response = await asyncio.to_thread(
            gemini_client.generate,
            prompt
        )

        if not response:
            return "No response from AI."

        return f"{response.strip()}\n\n---\n{_extract_sources(has_data)}"

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."