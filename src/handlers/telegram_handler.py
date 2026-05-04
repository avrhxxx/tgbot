# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: AI Coach Telegram handler (Sheets = registry, Firestore = knowledge layer)

import logging
import asyncio
from aiogram.types import Message

from src.ai.gemini import gemini_client

logger = logging.getLogger("handlers.telegram")


# =========================
# READ FROM SHEETS (FULL REGISTRY, NO LOSS)
# =========================
def get_game_state(sheets_client):
    """
    Sheets = SOURCE OF TRUTH (no filtering here!)
    We pass full graph to AI for semantic reasoning.
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

        for r in rows[1:]:
            if len(r) < 6:
                continue

            _type = r[1]
            name = r[2]
            parent_name = r[5]

            if _type == "hero":
                heroes.append(name)

            elif _type == "skill":
                skills.append({
                    "name": name,
                    "hero": parent_name
                })

            elif _type == "building":
                buildings.append(name)

        return heroes, skills, buildings

    except Exception as e:
        logger.exception("❌ Sheets read error: %s", e)
        return [], [], []


# =========================
# PROMPT BUILDER (COACH v3 - CLEAN GRAPH MODE)
# =========================
def build_prompt(user_text: str, state):
    heroes, skills, buildings = state

    return f"""
You are an advanced GAME COACH AI.

========================
SYSTEM DESIGN
========================

You operate on structured game registry:

- HEROES = characters in game
- SKILLS = abilities linked to heroes
- BUILDINGS = world structures

You must use relationship data:
- skill.hero defines ownership

========================
IMPORTANT RULES
========================

- NEVER hallucinate missing data
- If mechanics are unknown → say:
  "This exists in the game, but is not documented yet."
- Use relationships to group skills under heroes
- Do NOT assume global skill pool

========================
GAME REGISTRY
========================

HEROES:
{heroes}

SKILLS:
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

    # FULL GRAPH (no filtering)
    state = get_game_state(sheets_client)

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