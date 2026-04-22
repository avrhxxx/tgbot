from src.engine.transition_engine import TransitionEngine


class ActionHandler:
    """
    Mapuje akcje użytkownika → transition engine
    """

    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def handle(self, state: dict, action: str) -> dict:
        """
        Główne wejście:
        kliknięcie / akcja UI → nowy state
        """
        new_state = self.transition_engine.transition(state, action)
        return new_state