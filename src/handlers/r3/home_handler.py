# src/handlers/r3/home_handler.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

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
    # STATE SYSTEM (SOURCE OF TRUTH)
    # =========================
    session = app.session_engine.get(user_id)
    game_nick = session.get("game_nick")

    role = user_service.get_role(user_id)

    first_name = (
        message.from_user.first_name
        or message.from_user.username
        or "User"
    )

    # =========================
    # ONBOARDING
    # =========================
    if game_nick is None:
        app.set_session_state(user_id, "awaiting_nick")

        await message.answer(
            "🎮 Welcome!\n\n"
            "Send your Game Nick:"
        )
        return

    # =========================
    # HOME
    # =========================
    text = nav_service.get_home_screen(
        first_name=first_name,
        role=role,
        game_nick=game_nick
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Events",
                    callback_data="nav.events"
                ),
                InlineKeyboardButton(
                    text="⚡ Quick Join",
                    callback_data="nav.quick_join"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Settings",
                    callback_data="nav.settings"
                ),
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="nav.help"
                ),
            ],
        ]
    )

    await message.answer(text, reply_markup=keyboard)