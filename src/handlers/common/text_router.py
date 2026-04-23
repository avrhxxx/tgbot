# src/handlers/common/text_router.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def text_router(message: Message, **data):
    """
    GLOBAL TEXT HANDLER (FSM-lite)

    Handles:
    - onboarding nick input
    - future text flows
    """

    app = data.get("app")
    if app is None:
        return

    user_id = str(message.from_user.id)

    session = app.get_session(user_id)
    user_service = app.services.get("user")

    if user_service is None:
        return

    # =========================
    # CASE 1: WAITING FOR GAME NICK
    # =========================
    if session and session.get("state") == "awaiting_nick":
        nick = message.text.strip()

        if len(nick) < 2:
            await message.answer("❌ Nick too short. Try again:")
            return

        if len(nick) > 20:
            await message.answer("❌ Nick too long (max 20 chars). Try again:")
            return

        # SAVE NICK
        user_service.set_game_nick(user_id, nick)

        # CLEAR SESSION STATE
        app.delete_session(user_id)

        await message.answer(f"✅ Nick set: {nick}")

        # REDIRECT TO HOME FLOW (trigger /start logic manually)
        from src.handlers.r3.home_handler import home
        await home(message, app=app)

        return

    # =========================
    # DEFAULT FALLBACK
    # =========================
    await message.answer("🤖 Unknown command. Use /start")