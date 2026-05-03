# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: User AI Coach handler (multi-source READ: Sheets + Firestore future-ready)

import logging
from aiogram.types import Message

from src.ai.gemini import gemini_client

logger = logging.getLogger("handlers.telegram")


# =========================
# READ FROM SHEETS
# =========================
def get_game_state(sheets_client):
    if not sheets_client:
        return [], [], []

    try:
        result = sheets_client.service.spreadsheets().values().get(
            spreadsheetId=sheets_client.sheet_id,
            range="indexes!A:F",
        ).execute()

        rows = result.get("values", [])

        heroes, skills, buildings = [], [], []

        for r in rows[1:]:
            if len(r) < 3:
                continue

            t = r[1]
            name = r[2]

            if t == "hero":
                heroes.append(name)
            elif t == "skill":
                skills.append(name)
            elif t == "building":
                buildings.append(name)

        return heroes, skills, buildings

    except Exception as e:
        logger.exception("❌ Sheets read error: %s", e)
        return [], [], []


# =========================
# PROMPT BUILDER (COACH v2)
# =========================
def build_prompt(user_text: str, state):
    heroes, skills, buildings = state

    return f"""
You are an advanced GAME COACH AI.

You MUST follow these rules:

========================
1. LANGUAGE RULE
========================
Respond in the SAME language as the user message.

========================
2. DATA SOURCES
========================
You have access to:

- INDEX DATABASE (authoritative list of entities)
- FIRESTORE (mechanics & descriptions, currently may be empty)

========================
3. CURRENT INDEX DATABASE
========================

HEROES:
{heroes}

SKILLS:
{skills}

BUILDINGS:
{buildings}

========================
4. FIRESTORE RULE
========================
- If mechanic/description exists → use it
- If NOT available → say:
  "This exists in the game, but mechanics are not yet documented."

========================
5. BEHAVIOR RULES
========================
- Do NOT invent stats or mechanics
- You can confirm existence from INDEXES
- You can explain missing data as "not yet known"
- Be concise and helpful like a game wiki assistant

========================
USER QUESTION
========================
{user_text}
"""


# =========================
# USER HANDLER
# =========================
async def handle_message(message: Message):

    text = message.text or ""
    logger.info("📩 USER QUERY: %s", text)

    sheets_client = message.bot.__dict__.get("sheets_client")

    # load game state
    state = get_game_state(sheets_client)

    # build prompt
    prompt = build_prompt(text, state)

    try:
        response = gemini_client.generate(prompt)
        await message.answer(response)

    except Exception as e:
        logger.exception("❌ AI coach error")
        await message.answer(f"AI error: {e}")