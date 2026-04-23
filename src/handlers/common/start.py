# src/handlers/common/start.py

from aiogram import types

from src.engine.state_machine import UserState


async def start_handler(message: types.Message, app):
    """
    Entry point for /start command.
    Initializes user onboarding flow.
    """

    if message.from_user is None:
        return

    user_id = str(message.from_user.id)

    session_engine = app.session_engine
    if session_engine is None:
        return

    engine = app.ui.get("engine")
    if engine is None:
        return

    user_service = app.services.get("user")
    if user_service is None:
        return

    first_name = message.from_user.first_name or "User"

    # =========================
    # INIT STATE (CLEAN FLOW)
    # =========================
    current_state = session_engine.get_state(user_id)

    # If brand new user → start onboarding
    if current_state == UserState.NEW:
        session_engine.set_state(user_id, UserState.AWAITING_NICK)

    # =========================
    # FETCH UPDATED STATE DATA
    # =========================
    state_data = session_engine.get(user_id) or {}

    # =========================
    # RESOLVE ROLE
    # =========================
    role = user_service.get_role(user_id)

    # =========================
    # RENDER HOME SCREEN
    # =========================
    view = await engine.render(
        "home",
        app=app,
        user_id=user_id,
        first_name=first_name,
        role=role,
        game_nick=state_data.get("nick"),
        callback=message,
    )

    await message.answer(
        text=view["text"],
        reply_markup=view["keyboard"],
    )