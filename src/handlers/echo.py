from aiogram import Router
from aiogram.types import Message

from src.core.dispatcher import dispatch
from src.core.state import UIState
from src.core.actions import Action

router = Router()

_state_store: dict[int, UIState] = {}


def map_text_to_action(text: str | None) -> Action:
    if not text:
        return Action.GO_HOME

    text = text.lower()

    if text in ["home", "start", "a", ""]:
        return Action.GO_HOME

    if text in ["event", "open"]:
        return Action.OPEN_EVENT

    if text in ["back"]:
        return Action.BACK

    return Action.GO_HOME


@router.message()
async def process_any_message(message: Message):
    user_id = message.from_user.id

    # LOAD STATE
    state = _state_store.get(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # MAP INPUT → ACTION
    action = map_text_to_action(message.text)

    # DISPATCH
    new_state = dispatch(action, state)

    # SAVE STATE
    _state_store[user_id] = new_state

    # RESPONSE
    await message.reply(
        text=(
            f"🧠 STATE UPDATED\n"
            f"screen: {new_state.screen}\n"
            f"role: {new_state.role}"
        )
    )