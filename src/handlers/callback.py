from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.core.state import UIState
from src.core.router import resolve_screen
from src.core.state_store import state_store

from src.engine.action_handler import ActionHandler
from src.engine.bootstrap_state_machine import build_state_machine
from src.engine.transition_engine import TransitionEngine

# NEW: UI CONTRACT LAYER
from src.ui.definitions.action_ids import ActionID

router = Router()

# =========================
# ENGINE INIT (SINGLE SOURCE OF TRUTH)
# =========================
state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)


# =========================
# UI ID → ACTION MAP
# =========================
UI_TO_ACTION_MAP = {
    # NAVIGATION
    ActionID.GO_HOME: ActionID.GO_HOME,
    ActionID.GO_EVENTS: ActionID.GO_EVENTS,
    ActionID.GO_SETTINGS: ActionID.GO_SETTINGS,
    ActionID.BACK: ActionID.BACK,

    # EVENTS
    ActionID.JOIN_EVENT: ActionID.JOIN_EVENT,
    ActionID.OPEN_EVENT: ActionID.OPEN_EVENT,
    ActionID.LEAVE_EVENT: ActionID.LEAVE_EVENT,

    # EVENT MANAGEMENT
    ActionID.GO_EVENT_MANAGEMENT: ActionID.GO_EVENT_MANAGEMENT,
    ActionID.CREATE_EVENT: ActionID.CREATE_EVENT,

    # SETTINGS
    ActionID.CHANGE_GAME_NICK: ActionID.CHANGE_GAME_NICK,

    # DEMO
    ActionID.DEMO_SWITCH_ROLE: ActionID.DEMO_SWITCH_ROLE,
}


# =========================
# DEMO SWITCH HANDLER
# =========================
def handle_demo_switch(user_id: int, data: str) -> bool:
    if not data.startswith("demo:switch_role:"):
        return False

    role = data.split(":")[2]
    state_store.set_demo_role(user_id, role)

    return True


# =========================
# MAIN HANDLER
# =========================
@router.callback_query(F.data)
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    # =========================
    # DEMO MODE BRANCH (PRE-FSM)
    # =========================
    if handle_demo_switch(user_id, data):
        state = state_store.get(user_id)

        if state:
            screen_payload = resolve_screen(state.screen, state)

            await callback.message.edit_text(
                text=screen_payload.get("text", "No UI"),
                reply_markup=screen_payload.get("keyboard"),
            )

        await callback.answer()
        return

    # =========================
    # LOAD STATE
    # =========================
    state = state_store.get_or_create(
        user_id,
        UIState(
            user_id=user_id,
            screen="home_r3",
            role="R3",
        ),
    )

    # =========================
    # UI → ACTION RESOLVE
    # =========================
    action = UI_TO_ACTION_MAP.get(data)

    if action is None:
        await callback.answer()
        return

    # =========================
    # FSM TRANSITION
    # =========================
    new_state = await handler.handle(state, action)

    # =========================
    # SAVE STATE
    # =========================
    state_store.set(user_id, new_state)

    # =========================
    # RENDER SCREEN
    # =========================
    screen_payload = resolve_screen(new_state.screen, new_state)

    new_text = screen_payload.get("text", "No UI")
    new_kb = screen_payload.get("keyboard")

    current_text = callback.message.text if callback.message else None
    current_kb = callback.message.reply_markup if callback.message else None

    # NO-OP GUARD
    if current_text == new_text and current_kb == new_kb:
        await callback.answer()
        return

    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=new_kb,
        )
    except Exception as e:
        if "message is not modified" not in str(e):
            raise

    await callback.answer()