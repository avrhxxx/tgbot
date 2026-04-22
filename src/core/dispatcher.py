from src.engine.transition_engine import TransitionEngine


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


def dispatch(action, state):
    if _dispatcher is None:
        raise RuntimeError("Dispatcher not initialized")

    return _dispatcher.dispatch(action, state)