# src/handlers/r3/home_handler.py

from aiogram import Router, F

router = Router()


@router.message(F.text == "/start")
async def home(message, app):
    user_id = str(message.from_user.id)

    user_service = app.services["user"]
    nav_service = app.services["nav"]

    role = user_service.get_role(user_id)

    text = nav_service.get_home_screen(
        role=role,
        demo_mode=app.is_demo()
    )

    keyboard = []

    # DEMO SWITCH BUTTON (ONLY IF ENABLED)
    if app.is_demo():
        keyboard.append([
            nav_service.get_switch_roles_button()
        ])

    await message.answer(
        text,
        reply_markup={"inline_keyboard": keyboard}
    )