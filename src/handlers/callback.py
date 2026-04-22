from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.core.state import UIState
from src.core.router import resolve_screen
from src.core.state_store import state_store

from src.engine.action_handler import ActionHandler
from src.engine.bootstrap_state_machine import build_state_machine
from src.engine.transition_engine import TransitionEngine

from src.ui.definitions.action_ids import ActionID
from src.core.role_cycle import get_next_role

router = Router()

# =========================
# ENGINE INIT
# =========================
state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)


# =========================
# UI → ACTION MAP
# =========================
UI_TO_ACTION_MAP = {
    ActionID.GO_HOME: ActionID.GO_HOME,
    ActionID.GO_EVENTS: ActionID.GO_EVENTS,
    ActionID.GO_SETTINGS: ActionID.GO_SETTINGS,
    ActionID.BACK: ActionID.BACK,

    ActionID.JOIN_EVENT: ActionID.JOIN_EVENT,
    ActionID.OPEN_EVENT: ActionID.OPEN_EVENT,
    ActionID.LEAVE_EVENT: ActionID.LEAVE_EVENT,

    ActionID.GO_EVENT_MANAGEMENT: ActionID.GO_EVENT_MANAGEMENT,
    ActionID.CREATE_EVENT: ActionID.CREATE_EVENT,

    ActionID.CHANGE_GAME_NICK: ActionID.CHANGE_GAME_NICK,
}


# =========================
# MAIN HANDLER
# =========================
@router.callback_query(F.data)
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    # =========================
    # LOAD STATE
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
    # 🎭 ROLE SWITCH (PRE-FSM SAFE PATH)
    # =========================
    if data == ActionID.SWITCH_ROLE:
        next_role = get_next_role(state.role)

        state = UIState(
            user_id=state.user_id,
            screen=state.screen,
            role=next_role,
        )

        state_store.set(user_id, state)

        screen_payload = resolve_screen(state.screen, state)

        try:
            await callback.message.edit_text(
                text=screen_payload.get("text", "No UI"),
                reply_markup=screen_payload.get("keyboard"),
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise

        await callback.answer()
        return

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

    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=new_kb,
        )
    except TelegramBadRequest as e:
        # 🔥 CRITICAL FIX: ignore identical render crash
        if "message is not modified" not in str(e):
            raise

    await callback.answer()