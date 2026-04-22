from aiogram import Router
from aiogram.types import Message

from src.core.dispatcher import dispatch
from src.core.state import UIState
from src.core.actions import Action

router = Router()

_state_store: dict[int, UIState] = {}


@router.message()
async def process_any_message(message: Message):
    user_id = message.from_user.id

    # 1. LOAD STATE
    state = _state_store.get(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # 2. MAP INPUT → ACTION (NA RAZIE PROSTO)
    action = Action.from_text(message.text)

    # 3. PASS TO ENGINE
    new_state = await dispatch(action, state)

    # 4. SAVE STATE
    _state_store[user_id] = new_state

    # 5. RESPONSE
    await message.reply(
        text=(
            f"🧠 STATE UPDATED\n"
            f"screen: {new_state.screen}\n"
            f"role: {new_state.role}"
        )
    )