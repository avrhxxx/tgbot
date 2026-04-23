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
        # ROLE ACTION
        # =========================
        if isinstance(callback, RoleCB):
            # role switching is handled outside FSM in router
            return state

        # =========================
        # NAVIGATION ACTION
        # =========================
        if isinstance(callback, NavigationCB):

            # BACK logic
            if callback.target == "back":
                history = getattr(state, "history", [])

                if history:
                    previous_screen = history.pop()
                    state.screen = previous_screen
                    state.history = history

                return state

            # FORWARD STACK
            history = getattr(state, "history", [])
            history.append(state.screen)
            state.history = history

            # screen transition = navigation target
            return self.transition_engine.transition(state, callback.target)

        # =========================
        # EVENT ACTION
        # =========================
        if isinstance(callback, EventCB):

            # FORWARD STACK
            history = getattr(state, "history", [])
            history.append(state.screen)
            state.history = history

            # FSM TRANSITION
            return self.transition_engine.transition(
                state,
                f"event:{callback.action}"
            )

        # =========================
        # FALLBACK (SAFE NO-OP)
        # =========================
        return state