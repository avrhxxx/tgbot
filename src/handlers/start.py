from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.core.state import UIState
from src.core.router import resolve_screen
from src.core.state_store import state_store

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id

    # =========================
    # 🧠 INIT STATE (ONLY IF MISSING)
    # =========================
    state = state_store.get_or_create(
        user_id,
        UIState(
            user_id=user_id,
            screen="home",
            role="R3",
        ),
    )

    # =========================
    # 🚫 NIE NADPISUJ TEGO BEZ POWODU
    # =========================
    # wcześniej: state.screen = "home" (to było redundantne)

    state_store.set(user_id, state)

    # =========================
    # 🧠 RENDER FIRST SCREEN
    # =========================
    screen_payload = resolve_screen(state.screen, state)

    await message.answer(
        text=screen_payload.get("text", "No UI"),
        reply_markup=screen_payload.get("keyboard")
    )