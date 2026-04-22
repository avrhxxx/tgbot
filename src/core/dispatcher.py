from src.engine.transition_engine import TransitionEngine


class Dispatcher:
    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def dispatch(self, action, state):
        return self.transition_engine.transition(state, action)


# =====================================
# 🔥 COMPATIBILITY LAYER (ETAP 3 SAFE)
# =====================================

_dispatcher_instance: Dispatcher | None = None


def init_dispatcher(transition_engine: TransitionEngine):
    global _dispatcher_instance
    _dispatcher_instance = Dispatcher(transition_engine)


async def dispatch(action, state):
    """
    Funkcyjny wrapper dla starego importu:
    echo.py → dispatch(...)
    """
    return await _dispatcher_instance.dispatch(action, state)