
# src/handlers/common/callback_router.py

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "demo.switch_role")
async def switch_role(callback: CallbackQuery, **data):
    app = data.get("app")
    if app is None:
        raise RuntimeError("App context not found in callback")

    user_id = str(callback.from_user.id)

    user_service = app.services["user"]

    # =========================
    # ROLE SWITCH (BUSINESS LOGIC ONLY)
    # =========================
    current_role = user_service.get_role(user_id)
    new_role = user_service.cycle_role(current_role)
    user_service.set_role(user_id, new_role)

    # =========================
    # SCREEN SYSTEM RENDER
    # =========================
    engine = app.ui["engine"]

    view = await engine.render(
        "home",
        app=app,
        user_id=user_id,
        first_name=(
            callback.from_user.first_name
            or callback.from_user.username
            or "User"
        ),
        role=new_role,
        game_nick=None,
        callback=callback,
    )

    # =========================
    # UPDATE MESSAGE (SAFE UI OUTPUT)
    # =========================
    await callback.message.edit_text(
        view["text"],
        reply_markup=view["keyboard"]
    )

    await callback.answer()