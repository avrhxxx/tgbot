# src/handlers/r3/home_handler.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.engine.state_machine import UserState

router = Router()


@router.message(F.text == "/start")
async def home(message: Message, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in handler data. Check middleware injection.")

    user_id = str(message.from_user.id)

    # =========================
    # SAFE SERVICE ACCESS
    # =========================
    user_service = app.services.get("user")
    nav_service = app.services.get("nav")
    session_engine = app.session_engine

    if user_service is None or nav_service is None:
        await message.answer(
            "⚠️ Bot is not fully initialized yet.\nServices are not connected."
        )
        return

    # =========================
    # SESSION + STATE
    # =========================
    session = session_engine.get(user_id)
    state = session["state"]

    # =========================
    # FIRST TIME USER → ASK NICK
    # =========================
    if state == UserState.NEW:
        session_engine.set_state(user_id, UserState.AWAITING_NICK)

        await message.answer(
            "👋 Welcome!\nPlease enter your game nickname:"
        )
        return

    # =========================
    # AWAITING NICK BUT NOT SET
    # =========================
    if state == UserState.AWAITING_NICK and not session.get("game_nick"):
        await message.answer("✍️ Please type your game nickname:")
        return

    # =========================
    # NORMAL FLOW
    # =========================
    role = user_service.get_role(user_id)

    first_name = (
        message.from_user.first_name
        or message.from_user.username
        or "User"
    )

    text = nav_service.get_home_screen(
        first_name=first_name,
        role=role,
        game_nick=session.get("game_nick")
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="🔁 Switch Role (Only in Demo)",
                callback_data="demo.switch_role"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer(
        text,
        reply_markup=reply_markup
    )