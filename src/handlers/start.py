from aiogram import Router
from aiogram.types import Message

from src.core.state import UIState
from src.core.router import resolve_screen
from src.core.state_store import state_store

router = Router()


def resolve_home_by_role(role: str) -> str:
    """
    Maps user role → home screen
    """
    role = (role or "R3").upper()

    if role == "R5":
        return "home_r5"
    if role == "R4":
        return "home_r4"
    return "home_r3"


@router.message(commands=["start"])
async def start_command(message: Message):
    user_id = message.from_user.id

    # pobierz lub stwórz state usera
    state = state_store.get_or_create(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # role-based home routing
    state.screen = resolve_home_by_role(state.role)

    # zapis stanu
    state_store.set(user_id, state)

    # render UI
    screen_payload = resolve_screen(state.screen, state)

    await message.answer(
        text=screen_payload.get("text", "No UI"),
        reply_markup=screen_payload.get("keyboard")
    )