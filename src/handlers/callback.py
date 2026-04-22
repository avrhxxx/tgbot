from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.core.state import UIState
from src.core.actions import Action
from src.core.router import resolve_screen

from src.engine.action_handler import ActionHandler
from src.engine.bootstrap_state_machine import build_state_machine
from src.engine.transition_engine import TransitionEngine

router = Router()

# =========================
# ENGINE (TA SAMA LOGIKA CO W echo.py)
# =========================
state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)

_state_store: dict[int, UIState] = {}


# =========================
# CALLBACK → ACTION MAP
# =========================
def map_callback_to_action(data: str | None) -> Action:
    if not data:
        return Action.GO_HOME

    if data == "go_home":
        return Action.GO_HOME

    if data == "go_events":
        return Action.OPEN_EVENT

    if data == "go_settings":
        return Action.BACK  # (na razie placeholder, możesz później rozdzielić)

    if data == "back":
        return Action.BACK

    return Action.GO_HOME


# =========================
# MAIN HANDLER
# =========================
@router.callback_query(F.data)
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id

    # LOAD STATE (tymczasowo memory, potem przeniesiemy do shared store)
    state = _state_store.get(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # MAP CALLBACK → ACTION
    action = map_callback_to_action(callback.data)

    # FSM TRANSITION
    new_state = await handler.handle(state, action)

    _state_store[user_id] = new_state

    # UI RENDER
    screen_payload = resolve_screen(new_state.screen, new_state)

    # EDIT MESSAGE (ważne dla UX)
    await callback.message.edit_text(
        text=screen_payload.get("text", "No UI"),
        reply_markup=screen_payload.get("keyboard"),
    )

    await callback.answer()