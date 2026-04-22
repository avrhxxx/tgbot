from src.engine.transition_engine import TransitionEngine
from src.core.state_store import state_store
from src.core.actions import Action


class Dispatcher:
    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    def dispatch(self, action: Action, state):
        # DEBUG GUARD (critical for future bugs)
        if action is None:
            raise ValueError("Action is None")

        return self.transition_engine.transition(state, action)


_dispatcher = None


def init_dispatcher(transition_engine: TransitionEngine):
    global _dispatcher
    _dispatcher = Dispatcher(transition_engine)


def dispatch(action: Action, state, user_id: int | None = None):
    if _dispatcher is None:
        raise RuntimeError("Dispatcher not initialized")

    # =========================
    # DEMO MODE HOOK (SAFE COPY)
    # =========================
    if user_id is not None:
        demo_role = state_store.get_demo_role(user_id)

        if demo_role:
            state = _inject_demo_role(state, demo_role)

    return _dispatcher.dispatch(action, state)


def _inject_demo_role(state, role: str):
    """
    DO NOT MUTATE ORIGINAL STATE OBJECT
    """

    # copy-safe approach (prevents FSM cache bugs)
    if hasattr(state, "model_copy"):  # pydantic v2 style (if used)
        state = state.model_copy(deep=True)
    elif hasattr(state, "copy"):
        state = state.copy()
    else:
        # fallback: shallow copy safeguard
        import copy
        state = copy.copy(state)

    if hasattr(state, "role"):
        state.role = role

    return state