from src.engine.transition_engine import TransitionEngine
from src.core.actions import Action


class ActionHandler:
    """
    Mapuje akcje użytkownika → transition engine
    """

    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def handle(self, state, action: Action):
        """
        Główne wejście:
        kliknięcie / akcja UI → nowy state
        """

        # 🔥 NORMALIZACJA (KLUCZ FIX)
        if isinstance(action, Action):
            action = action.value

        new_state = self.transition_engine.transition(state, action)
        return new_state