from src.engine.transition_engine import TransitionEngine

from src.ui.callbacks.navigation import NavigationCB
from src.ui.callbacks.event import EventCB
from src.ui.callbacks.role import RoleCB


class ActionHandler:
    """
    Maps CallbackData → Transition Engine
    + manages navigation history stack
    """

    def __init__(self, transition_engine: TransitionEngine):
        self.transition_engine = transition_engine

    async def handle(self, state, callback):
        """
        CallbackData → State Transition FLOW
        """

        # =========================
        # ROLE ACTION (NO FSM)
        # =========================
        if isinstance(callback, RoleCB):
            return state

        # =========================
        # NAVIGATION ACTION
        # =========================
        if isinstance(callback, NavigationCB):

            # BACK logic
            if callback.target == "back":
                history = getattr(state, "history", [])

                if history:
                    state.screen = history.pop()
                    state.history = history

                return state

            # FORWARD STACK
            history = getattr(state, "history", [])
            history.append(state.screen)
            state.history = history

            # screen transition via UI routing
            return self.transition_engine.transition(state, callback.target)

        # =========================
        # EVENT ACTION
        # =========================
        if isinstance(callback, EventCB):

            history = getattr(state, "history", [])
            history.append(state.screen)
            state.history = history

            # FSM-like transition via engine
            return self.transition_engine.transition(
                state,
                f"event:{callback.action}"
            )

        # =========================
        # FALLBACK (SAFE NO-OP)
        # =========================
        return state