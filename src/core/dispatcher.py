from src.engine.transition_engine import TransitionEngine


class Dispatcher:
    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    def dispatch(self, action, state):
        return self.transition_engine.transition(state, action)