from aiogram import Router
from aiogram.types import Message

from src.core.state import UIState
from src.core.actions import Action
from src.core.router import resolve_screen

from src.engine.action_handler import ActionHandler
from src.engine.transition_engine import TransitionEngine
from src.engine.bootstrap_state_machine import build_state_machine

router = Router()

state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)

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

    state = _state_store.get(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    action = map_text_to_action(message.text)

    new_state = await handler.handle(state, action)

    _state_store[user_id] = new_state

    # 🧠 UI LAYER (NOWY KROK)
    screen_payload = resolve_screen(new_state.screen, new_state)

    await message.reply(
        text=screen_payload.get("text", "No UI"),
    )