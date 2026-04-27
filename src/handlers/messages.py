from aiogram import Router, types

from src.flows.announcement_flow import handle_message

router = Router()


@router.message()
async def message_router(message: types.Message):
    handled = await handle_message(message)

    if handled:
        return

    await message.answer("Unknown command")