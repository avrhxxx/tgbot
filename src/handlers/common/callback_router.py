# src/handlers/common/callback_router.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

router = Router()


@router.callback_query(F.data == "demo.switch_role")
async def switch_role(callback: CallbackQuery, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in callback")

    user_id = str(callback.from_user.id)

    # =========================
    # FIX: correct service key
    # =========================
    user_service = app.services["user_service"]

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
    # SCREEN ENGINE RENDER
    # =========================
    engine = app.ui["engine"]

    view = await engine.render(
        "home",
        app=app,
        user_id=user_id,
        first_name=first_name,
        role=new_role,
        game_nick=None,
        callback=callback,
    )

    # =========================
    # FIX: aiogram union-safe message handling
    # =========================
    message = callback.message

    if message is None:
        await callback.answer()
        return

    if not isinstance(message, Message):
        # InaccessibleMessage cannot be edited
        await callback.answer()
        return

    try:
        await message.edit_text(
            view["text"],
            reply_markup=view["keyboard"],
        )
    except Exception:
        await message.answer(
            view["text"],
            reply_markup=view["keyboard"],
        )

    await callback.answer()