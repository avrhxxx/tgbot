# src/handlers/r3/home_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(F.text == "/start")
async def home(message: Message, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in handler data. Check middleware injection.")

    user_id = str(message.from_user.id)

    # =========================
    # SAFE SERVICE ACCESS (TEMP FIX)
    # =========================
    user_service = app.services.get("user")
    nav_service = app.services.get("nav")

    # TEMP fallback (żeby bot nie crashował)
    if user_service is None or nav_service is None:
        await message.answer(
            "⚠️ Bot is not fully initialized yet.\nServices are not connected."
        )
        return

    # =========================
    # NORMAL FLOW
    # =========================
    role = user_service.get_role(user_id)

    text = nav_service.get_home_screen(
        role=role,
        demo_mode=app.is_demo()
    )

    keyboard = []

    if app.is_demo():
        keyboard.append([
            InlineKeyboardButton(
                text="Switch Roles",
                callback_data="switch_roles"
            )
        ])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer(
        text,
        reply_markup=reply_markup
    )