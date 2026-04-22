from aiogram import Router
from aiogram.types import Message

from src.core.actions import Action
from src.core.dispatcher import dispatch
from src.core.state import UIState

router: Router = Router()


# 🧠 TEMP: fake state storage (ETAP 2)
_state_store: dict[int, UIState] = {}


@router.message()
async def process_any_message(message: Message):
    user_id = message.from_user.id

    # =========================
    # INIT STATE IF NOT EXISTS
    # =========================
    state = _state_store.get(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # =========================
    # CORE DISPATCH LAYER
    # =========================
    state = await dispatch(Action.GO_HOME, state)

    _state_store[user_id] = state

    # =========================
    # TEMP RESPONSE (NO UI YET)
    # =========================
    await message.reply(
        text=(
            f"🧠 STATE UPDATED\n"
            f"screen: {state.screen}\n"
            f"role: {state.role}"
        )
    )