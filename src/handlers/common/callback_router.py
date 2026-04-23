
# src/handlers/common/callback_router.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.callback_query(F.data == "demo.switch_role")
async def switch_role(callback: CallbackQuery, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in callback")

    user_id = str(callback.from_user.id)

    user_service = app.services["user"]
    nav_service = app.services["nav"]

    # =========================
    # ROLE SWITCH
    # =========================
    current_role = user_service.get_role(user_id)
    new_role = user_service.cycle_role(current_role)
    user_service.set_role(user_id, new_role)

    # =========================
    # USER INFO
    # =========================
    first_name = (
        callback.from_user.first_name
        or callback.from_user.username
        or "User"
    )

    # =========================
    # RENDER UI
    # =========================
    text = nav_service.get_home_screen(
        first_name=first_name,
        role=new_role,
        game_nick=None
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔁 Switch Role",
                    callback_data="demo.switch_role"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()