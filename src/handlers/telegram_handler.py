# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: AI Coach Telegram handler (Smart Index Filtering + Sheets relation aware)

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
    Returns filtered game state based on query keywords.
    Prevents dumping full dataset into AI prompt.
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

        for r in rows[1:]:
            if len(r) < 6:
                continue

            _id = r[0]
            _type = r[1]
            name = r[2]
            slug = r[3]
            parent_type = r[4]
            parent_name = r[5]

            # =========================
            # HERO FILTER
            # =========================
            if _type == "hero":
                if query_lower in name.lower():
                    heroes.append(name)
                continue

            # =========================
            # SKILL FILTER (HERO RELATION AWARE)
            # =========================
            if _type == "skill":
                hero_match = parent_name and query_lower in parent_name.lower()
                name_match = query_lower in name.lower()

                if hero_match or name_match:
                    skills.append({
                        "name": name,
                        "hero": parent_name
                    })
                continue

            # =========================
            # BUILDINGS FILTER
            # =========================
            if _type == "building":
                if query_lower in name.lower():
                    buildings.append(name)

        return heroes, skills, buildings

    except Exception as e:
        logger.exception("❌ Sheets read error: %s", e)
        return [], [], []


# =========================
# PROMPT BUILDER (COACH v2 SMART)
# =========================
def build_prompt(user_text: str, state):
    heroes, skills, buildings = state

    return f"""
You are a GAME COACH AI assistant.

========================
RULES
========================
- Respond in the same language as the user
- Use ONLY provided filtered game data
- Do NOT invent mechanics or stats
- If data is missing, say it is not documented yet
- Be concise like a game wiki assistant

========================
FILTERED GAME DATA
========================

HEROES:
{heroes}

RELATED SKILLS (already filtered by hero relation):
{skills}

BUILDINGS:
{buildings}

========================
USER QUESTION
========================
{user_text}

========================
IMPORTANT NOTE
========================
Skills list is pre-filtered.
Do NOT assume full global skill database.
Only use what is provided above.
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

    # SMART FILTERED STATE (IMPORTANT CHANGE)
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