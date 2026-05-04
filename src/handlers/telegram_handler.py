# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: AI Coach Telegram handler (Sheets = registry, Firestore = knowledge layer)

import logging
import asyncio
from aiogram.types import Message

from src.ai.gemini import gemini_client

logger = logging.getLogger("handlers.telegram")


# =========================
# READ FROM SHEETS (SMART FILTER)
# =========================
def get_game_state(sheets_client, query: str):
    """
    Returns filtered game registry (ONLY existing game entities).
    Sheets = source of truth for existence, not mechanics.
    """
    if not sheets_client:
        return [], [], []

    try:
        result = sheets_client.service.spreadsheets().values().get(
            spreadsheetId=sheets_client.sheet_id,
            range="indexes!A:F",
        ).execute()

        rows = result.get("values", [])

        heroes = []
        skills = []
        buildings = []

        query_lower = query.lower()

        def match(q: str, t: str) -> bool:
            q_tokens = set(q.lower().split())
            t_tokens = set(t.lower().split())
            return len(q_tokens & t_tokens) > 0

        for r in rows[1:]:
            if len(r) < 6:
                continue

            _type = r[1]
            name = r[2]
            parent_name = r[5]

            # =========================
            # HEROES
            # =========================
            if _type == "hero":
                if match(query, name):
                    heroes.append(name)
                continue

            # =========================
            # SKILLS (RELATION AWARE)
            # =========================
            if _type == "skill":
                hero_match = parent_name and match(query, parent_name)
                name_match = match(query, name)

                if hero_match or name_match:
                    skills.append({
                        "name": name,
                        "hero": parent_name
                    })
                continue

            # =========================
            # BUILDINGS
            # =========================
            if _type == "building":
                if match(query, name):
                    buildings.append(name)

        return heroes, skills, buildings

    except Exception as e:
        logger.exception("❌ Sheets read error: %s", e)
        return [], [], []


# =========================
# PROMPT BUILDER (COACH v3 - DUAL LAYER SYSTEM)
# =========================
def build_prompt(user_text: str, state):
    heroes, skills, buildings = state

    return f"""
You are an advanced GAME COACH AI.

========================
GAME DATA MODEL (CRITICAL)
========================

You operate on TWO-LAYER SYSTEM:

1. INDEX LAYER (Sheets)
- defines what EXISTS in the game
- includes heroes, skills, buildings
- includes relationships (skill → hero)
- DOES NOT contain mechanics or explanations

2. KNOWLEDGE LAYER (Firestore)
- contains definitions of indexes
- explains what things do
- may be EMPTY for now
- if missing → explicitly say:
  "This exists in the game, but it is not documented yet."

========================
IMPORTANT RULE
========================
- NEVER invent mechanics or stats
- INDEX = existence only
- FIRESTORE = meaning only

========================
RELATIONSHIP RULE
========================
- Each skill belongs to exactly one hero
- Use this relation when answering questions
- Skills are NOT global pool

========================
FILTERED GAME DATA (INDEX LAYER)
========================

HEROES:
{heroes}

RELATED SKILLS:
{skills}

BUILDINGS:
{buildings}

========================
USER QUESTION
========================
{user_text}
"""


# =========================
# HANDLER
# =========================
async def handle_message(message: Message):
    text = message.text or ""

    logger.info("📩 USER QUERY: %s", text)

    if not text:
        await message.answer("Send a question.")
        return

    if text.startswith("/"):
        return

    sheets_client = message.bot.__dict__.get("sheets_client")

    # get ONLY relevant game registry
    state = get_game_state(sheets_client, text)

    prompt = build_prompt(text, state)

    try:
        response = await asyncio.to_thread(
            gemini_client.generate,
            prompt
        )

        if not response:
            await message.answer("No response from AI.")
            return

        await message.answer(response)

    except Exception as e:
        logger.exception("❌ AI coach error")
        await message.answer(f"AI error: {e}")