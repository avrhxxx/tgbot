# src/handlers/common/text_router.py

from aiogram import Router, F
from aiogram.types import Message

from src.engine.state_machine import UserState

router = Router()


@router.message(F.text)
async def text_router(message: Message, **data):
    """
    GLOBAL TEXT HANDLER (ONBOARDING + FUTURE FLOWS)
    """

    app = data.get("app")
    if app is None:
        return

    user_id = str(message.from_user.id)

    session_engine = app.session_engine

    if session_engine is None:
        return

    # =========================
    # SESSION LOAD (SINGLE SOURCE OF TRUTH)
    # =========================
    session = session_engine.get(user_id)
    state = session.get("state")

    # =========================
    # SAFETY: NULL STATE FIX
    # =========================
    if state is None:
        session_engine.set_state(user_id, UserState.NEW)
        state = UserState.NEW

    # =========================
    # CASE 1: AWAITING NICK
    # =========================
    if state == UserState.AWAITING_NICK:
        nick = message.text.strip()

        if len(nick) < 2:
            await message.answer("❌ Nick too short. Try again:")
            return

        if len(nick) > 20:
            await message.answer("❌ Nick too long (max 20 chars). Try again:")
            return

        # SAVE NICK (ONLY SESSION ENGINE)
        session_engine.set_nick(user_id, nick)

        # MOVE STATE → HOME
        session_engine.set_state(user_id, UserState.HOME)

        await message.answer(f"✅ Nick set: {nick}")

        # REDIRECT TO HOME FLOW
        from src.handlers.r3.home_handler import home
        await home(message, app=app)

        return

    # =========================
    # DEFAULT FALLBACK
    # =========================
    await message.answer("🤖 Unknown input. Use /start")