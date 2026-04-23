# src/handlers/common/callback_router.py

import logging
from aiogram import Router, F

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "demo.switch_role")
async def switch_role(callback, app):
    """
    DEMO ONLY ROLE SWITCH
    """

    user_id = str(callback.from_user.id)

    user_service = app.services["user"]
    nav_service = app.services["nav"]

    current = user_service.get_role(user_id)
    new_role = user_service.cycle_role(current)

    user_service.set_role(user_id, new_role)

    text = nav_service.get_home_screen(
        role=new_role,
        demo_mode=app.is_demo()
    )

    await callback.message.edit_text(text)
    await callback.answer("Role switched (DEMO)")