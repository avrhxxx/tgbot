# src/handlers/r3/home_handler.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(F.text == "/start")
async def home(message: Message, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in handler data. Check middleware injection.")

    user_id = str(message.from_user.id)

    # =========================
    # SERVICES
    # =========================
    user_service = app.services.get("user")
    nav_service = app.services.get("nav")

    if user_service is None or nav_service is None:
        await message.answer(
            "⚠️ Bot is not fully initialized yet.\nServices are not connected."
        )
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
    # 🚨 ONBOARDING GATE
    # =========================
    if game_nick is None:
        app.set_session(user_id, {"state": "awaiting_nick"})

        await message.answer(
            "🎮 Welcome!\n\n"
            "Before you continue, please set your Game Nick:\n\n"
            "👉 Send me your nickname in next message."
        )
        return

    # =========================
    # HOME SCREEN
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