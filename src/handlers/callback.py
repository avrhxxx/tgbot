from aiogram import Router
from aiogram.types import CallbackQuery

from src.core.state import UIState
from src.core.state_store import state_store
from src.core.router import resolve_screen

from src.engine.action_handler import ActionHandler
from src.engine.bootstrap_state_machine import build_state_machine
from src.engine.transition_engine import TransitionEngine

from src.core.role_cycle import get_next_role

from src.ui.callbacks.navigation import NavigationCB
from src.ui.callbacks.event import EventCB
from src.ui.callbacks.role import RoleCB

router = Router()

# ENGINE INIT
state_machine = build_state_machine()
transition_engine = TransitionEngine(state_machine)
handler = ActionHandler(transition_engine)


@router.callback_query()
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    state = state_store.get_or_create(
        user_id,
        UIState(user_id=user_id, screen="home", role="R3"),
    )

    # =========================
    # ROLE
    # =========================
    role_cb = RoleCB.parse(data)
    if role_cb:
        next_role = get_next_role(state.role)

        state.role = next_role
        state_store.set(user_id, state)

        payload = resolve_screen(state.screen, state)

        await callback.message.edit_text(
            text=payload["text"],
            reply_markup=payload["keyboard"],
        )
        await callback.answer()
        return

    # =========================
    # NAVIGATION
    # =========================
    nav_cb = NavigationCB.parse(data)
    if nav_cb:
        state.screen = nav_cb.target
        state_store.set(user_id, state)

        payload = resolve_screen(state.screen, state)

        await callback.message.edit_text(
            text=payload["text"],
            reply_markup=payload["keyboard"],
        )
        await callback.answer()
        return

    # =========================
    # EVENT
    # =========================
    event_cb = EventCB.parse(data)
    if event_cb:
        new_state = await handler.handle(state, event_cb.action)

        state_store.set(user_id, new_state)

        payload = resolve_screen(new_state.screen, new_state)

        await callback.message.edit_text(
            text=payload["text"],
            reply_markup=payload["keyboard"],
        )
        await callback.answer()
        return

    await callback.answer()