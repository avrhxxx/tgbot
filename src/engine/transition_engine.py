import logging
from src.engine.state_machine import StateMachine

logger = logging.getLogger(__name__)


class TransitionEngine:
    """
    Odpowiada za wykonanie zmiany stanu UI
    """

    def __init__(self, state_machine: StateMachine):
        self.state_machine = state_machine

    def transition(self, current_state, action):
        # UIState object access
        current_screen = current_state.screen

        next_screen = self.state_machine.get_next_screen(current_screen, action)

        if not next_screen:
            logger.warning(
                "No transition found: screen=%s action=%s",
                current_screen,
                action
            )
            return current_state

        # mutate state object (OK for now)
        current_state.screen = next_screen

        logger.info(
            "Transition: %s + %s -> %s",
            current_screen,
            action,
            next_screen
        )

        return current_state