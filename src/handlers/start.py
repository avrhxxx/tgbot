from aiogram import Router, types
from aiogram.filters import CommandStart

from src.flows.announcement_flow import start_flow

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("📣 Ready")