# src/handlers/r3/home_handler.py

from aiogram import Router, F
from aiogram.types import Message

from src.engine.state_machine import UserState

router = Router()


@router.message(F.text == "/start")
async def home(message: Message, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found")

    user_id = str(message.from_user.id)

    user_service = app.services.get("user")
    nav_service = app.services.get("nav")

    if user_service is None or nav_service is None:
        await message.answer("⚠️ Bot not initialized")
        return

    # =========================
    # USER DATA
    # =========================
    role = user_service.get_role(user_id)
    game_nick = user_service.get_game_nick(user_id)

    first_name = (
        message.from_user.first_name
        or message.from_user.username
        or "User"
    )

    # =========================
    # ONBOARDING
    # =========================
    if game_nick is None:
        app.session_engine.set_state(user_id, UserState.AWAITING_NICK)

        await message.answer(
            "Welcome!\n\n"
            "Send your Game Nick:"
        )
        return

    # =========================
    # HOME VIEW (COMPOSED)
    # =========================
    view = nav_service.get_home_view(
        first_name=first_name,
        role=role,
        game_nick=game_nick,
        is_demo=app.is_demo(),
    )

    await message.answer(
        view["text"],
        reply_markup=view["keyboard"]
    )