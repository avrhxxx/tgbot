from src.engine.transition_engine import TransitionEngine


class Dispatcher:
    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    def dispatch(self, action, state):
        return self.transition_engine.transition(state, action)


# -----------------------------
# GLOBAL SINGLETON (MVP HOOK)
# -----------------------------
_dispatcher_instance = None


def init_dispatcher(transition_engine: TransitionEngine):
    """
    Wywołujesz raz przy starcie bota.
    """
    global _dispatcher_instance
    _dispatcher_instance = Dispatcher(transition_engine)


def dispatch(action, state):
    """
    Funkcyjny entrypoint używany w handlers (np. echo.py)
    """
    if _dispatcher_instance is None:
        raise RuntimeError("Dispatcher not initialized")

    return _dispatcher_instance.dispatch(action, state)