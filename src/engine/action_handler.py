from src.engine.transition_engine import TransitionEngine
from src.ui.definitions.action_ids import ActionID


class ActionHandler:
    """
    Mapuje akcje użytkownika → transition engine
    + zarządza historią nawigacji (BACK system)
    """

    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def handle(self, state, action: str):
        """
        UI Action → State Transition (FULL FLOW)
        """

        # =========================
        # BACK LOGIC
        # =========================
        if action == ActionID.BACK:
            history = getattr(state, "history", [])

            if history:
                previous_screen = history.pop()
                state.screen = previous_screen
                state.history = history

            return state

        # =========================
        # FORWARD STACK
        # =========================
        history = getattr(state, "history", [])
        history.append(state.screen)
        state.history = history

        # =========================
        # FSM TRANSITION
        # =========================
        new_state = self.transition_engine.transition(state, action)

        return new_state