# src/handlers/common/text_router.py

from aiogram import Router, F
from aiogram.types import Message

from src.engine.state_machine import UserState

router = Router()


@router.message(F.text)
async def text_router(message: Message, **data):
    app = data.get("app")
    if app is None:
        return

    if message.from_user is None:
        return

    if message.text is None:
        return

    user_id = str(message.from_user.id)
    session_engine = app.session_engine

    if session_engine is None:
        return

    session = session_engine.get(user_id) or {}

    state = session.get("state")

    if state is None:
        session_engine.set_state(user_id, UserState.NEW)
        state = UserState.NEW

    # =========================
    # CASE: NICK INPUT
    # =========================
    if state == UserState.AWAITING_NICK:
        nick = message.text.strip()

        if len(nick) < 2:
            await message.answer("❌ Nick too short. Try again:")
            return

        if len(nick) > 20:
            await message.answer("❌ Nick too long (max 20 chars). Try again:")
            return

        session_engine.set_nick(user_id, nick)
        session_engine.set_state(user_id, UserState.HOME)

        await message.answer(f"✅ Nick set: {nick}")

        # 🔥 SCREEN SYSTEM ENTRY POINT
        engine = app.ui.get("engine")
        if engine is None:
            return

        user_service = app.services.get("user")
        if user_service is None:
            return

        view = await engine.render(
            "home",
            app=app,
            user_id=user_id,
            first_name=message.from_user.first_name or "User",
            role=user_service.get_role(user_id),
            game_nick=nick,
            callback=message,
        )

        await message.answer(
            view["text"],
            reply_markup=view["keyboard"]
        )

        return

    # =========================
    # DEFAULT → HOME SCREEN
    # =========================
    engine = app.ui.get("engine")
    if engine is None:
        return

    user_service = app.services.get("user")
    if user_service is None:
        return

    view = await engine.render(
        "home",
        app=app,
        user_id=user_id,
        first_name=message.from_user.first_name or "User",
        role=user_service.get_role(user_id),
        game_nick=session.get("nick"),
        callback=message,
    )

    await message.answer(
        view["text"],
        reply_markup=view["keyboard"]
    )