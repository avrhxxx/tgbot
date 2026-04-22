from src.engine.transition_engine import TransitionEngine
from src.core.state_store import state_store


class Dispatcher:
    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    def dispatch(self, action, state):
        return self.transition_engine.transition(state, action)


# 🔥 GLOBAL SINGLETON (MVP FIX)
_dispatcher = None


def init_dispatcher(transition_engine: TransitionEngine):
    global _dispatcher
    _dispatcher = Dispatcher(transition_engine)


def dispatch(action, state, user_id: int | None = None):
    """
    Extended dispatch with DEMO MODE support.
    """

    if _dispatcher is None:
        raise RuntimeError("Dispatcher not initialized")

    # =========================
    # DEMO MODE HOOK
    # =========================
    if user_id is not None:
        demo_role = state_store.get_demo_role(user_id)

        if demo_role:
            # override state role temporarily (non-destructive)
            state = _inject_demo_role(state, demo_role)

    return _dispatcher.dispatch(action, state)


def _inject_demo_role(state, role: str):
    """
    Lightweight state mutation for demo mode only.
    Never touches DB or real user data.
    """

    # zakładamy że state ma .role lub podobne pole
    if hasattr(state, "role"):
        state.role = role

    return state