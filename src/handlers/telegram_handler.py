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

        heroes = []
        skills = []
        buildings = []

        # IMPORTANT: structured extraction with relations
        for r in rows[1:]:
            if len(r) < 3:
                continue

            entity_type = r[1]
            name = r[2]

            parent_type = r[4] if len(r) > 4 else None
            parent_name = r[5] if len(r) > 5 else None

            if entity_type == "hero":
                heroes.append(name)

            elif entity_type == "skill":
                # store with relation for filtering in prompt
                skills.append({
                    "name": name,
                    "parent": parent_name
                })

            elif entity_type == "building":
                buildings.append(name)

        return heroes, skills, buildings

    except Exception as e:
        logger.exception("❌ Sheets read error: %s", e)
        return [], [], []


# =========================
# PROMPT BUILDER (COACH v3 - RELATIONAL + FIRESTORE)
# =========================
def build_prompt(user_text: str, state):
    heroes, skills, buildings = state

    return f"""
You are a STRICT GAME COACH AI.

You work like a DATABASE QUERY ENGINE + GAME WIKI.

========================
LANGUAGE RULE
========================
Respond in the same language as the user.

========================
DATA MODEL
========================
You have structured game data:

HEROES:
{heroes}

SKILLS (structured):
{skills}

BUILDINGS:
{buildings}

========================
RELATION RULE (CRITICAL)
========================
Skills are linked to heroes via:
- skill.parent == hero name

If user asks:
"skills of X"

YOU MUST:
- filter skills where parent == X
- ignore all other skills

NEVER use full skill list unless explicitly requested.

========================
FIRESTORE KNOWLEDGE LAYER
========================
Firestore contains:
- descriptions
- mechanics
- stats
- scaling
BUT MAY BE EMPTY

RULES:
- If Firestore data exists → use it
- If missing → say:
  "This exists in the game, but its mechanics are not yet documented."

NEVER INVENT MECHANICS.

========================
ANSWER RULES
========================
- Be precise
- Do not hallucinate
- Use only filtered data
- If unknown → say it is not documented
- Act like a game wiki assistant

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

    # load structured state
    state = get_game_state(sheets_client)

    prompt = build_prompt(text, state)

    try:
        response = gemini_client.generate(prompt)
        await message.answer(response)

    except Exception as e:
        logger.exception("❌ AI coach error")
        await message.answer(f"AI error: {e}")