from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.core.state import UIState
from src.core.actions import Action
from src.core.router import resolve_screen
from src.core.state_store import state_store

from src.engine.action_handler import ActionHandler
from src.engine.bootstrap_state_machine import build_state_machine
from src.engine.transition_engine import TransitionEngine

router = Router()

# =========================
# ENGINE (SINGLE SOURCE OF TRUTH)
# =========================
state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)


# =========================
# CALLBACK → ACTION MAP
# =========================
def map_callback_to_action(data: str | None) -> Action:
    if not data:
        return Action.GO_HOME

    mapping = {
        "go_home": Action.GO_HOME,
        "go_events": Action.OPEN_EVENT,
        "go_settings": Action.GO_HOME,  # placeholder
        "back": Action.BACK,
    }

    return mapping.get(data, Action.GO_HOME)


# =========================
# MAIN HANDLER
# =========================
@router.callback_query(F.data)
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id

    # LOAD STATE
    state = state_store.get_or_create(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # ACTION
    action = map_callback_to_action(callback.data)

    # FSM
    new_state = await handler.handle(state, action)

    # SAVE STATE
    state_store.set(user_id, new_state)

    # RENDER UI
    screen_payload = resolve_screen(new_state.screen, new_state)

    new_text = screen_payload.get("text", "No UI")
    new_kb = screen_payload.get("keyboard")

    # =========================
    # SAFE UI UPDATE (NO DUPES)
    # =========================
    current_text = callback.message.text if callback.message else None
    current_kb = callback.message.reply_markup if callback.message else None

    if current_text == new_text and current_kb == new_kb:
        await callback.answer()
        return

    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=new_kb,
        )
    except Exception as e:
        # ignore only harmless Telegram duplicate error
        if "message is not modified" not in str(e):
            raise

    await callback.answer()