from src.engine.transition_engine import TransitionEngine
from src.core.actions import Action


class ActionHandler:
    """
    Mapuje akcje użytkownika → transition engine
    + zarządza historią nawigacji (BACK system)
    """

    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def handle(self, state, action: Action):
        """
        UI Action → State Transition (FULL TYPE-SAFE FLOW)
        """

        # =========================
        # 🧭 BACK LOGIC (NAVIGATION STACK)
        # =========================
        if action == Action.BACK:
            history = getattr(state, "history", [])

            if history:
                previous_screen = history.pop()
                state.screen = previous_screen
                state.history = history

            return state

        # =========================
        # 🧭 FORWARD NAVIGATION STACK
        # =========================
        history = getattr(state, "history", [])

        # zapisz aktualny screen przed zmianą
        history.append(state.screen)
        state.history = history

        # =========================
        # 🔥 FSM TRANSITION
        # =========================
        new_state = self.transition_engine.transition(state, action)

        return new_state