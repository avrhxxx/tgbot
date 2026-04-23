# src/handlers/common/start.py

from aiogram import types

from src.engine.state_machine import UserState


async def start_handler(message: types.Message, app):

    if message.from_user is None:
        return

    user_id = str(message.from_user.id)

    session_engine = app.session_engine
    if session_engine is None:
        return

    # =========================
    # INIT USER STATE
    # =========================
    session_engine.set_state(user_id, UserState.HOME)

    engine = app.ui.get("engine")
    if engine is None:
        return

    user_service = app.services.get("user")
    if user_service is None:
        return

    first_name = message.from_user.first_name or "User"

    view = await engine.render(
        "home",
        app=app,
        user_id=user_id,
        first_name=first_name,
        role=user_service.get_role(user_id),
        game_nick=session_engine.get(user_id).get("nick"),
        callback=message,
    )

    await message.answer(
        text=view["text"],
        reply_markup=view["keyboard"]
    )