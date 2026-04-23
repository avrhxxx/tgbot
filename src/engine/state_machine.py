# src/engine/state_machine.py

import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("shadow.engine.state_machine")


# =========================
# USER FLOW STATES
# =========================
class UserState(str, Enum):
    """
    Global user lifecycle states.
    """

    NEW = "new"
    AWAITING_NICK = "awaiting_nick"
    HOME = "home"
    IN_EVENT = "in_event"
    IN_SQUAD = "in_squad"


# =========================
# STATE TRANSITIONS RULES
# =========================
ALLOWED_TRANSITIONS: dict[UserState, set[UserState]] = {
    UserState.NEW: {
        UserState.AWAITING_NICK,
    },

    UserState.AWAITING_NICK: {
        UserState.HOME,
        UserState.AWAITING_NICK,
    },

    UserState.HOME: {
        UserState.IN_EVENT,
        UserState.AWAITING_NICK,
        UserState.HOME,
    },

    UserState.IN_EVENT: {
        UserState.HOME,
        UserState.IN_SQUAD,
        UserState.IN_EVENT,
    },

    UserState.IN_SQUAD: {
        UserState.HOME,
        UserState.IN_SQUAD,
    },
}


# =========================
# STATE MACHINE CORE
# =========================
@dataclass
class StateMachine:
    """
    Responsible for validating and controlling user state transitions.
    """

    def can_transition(self, current: UserState, new: UserState) -> bool:
        if current == new:
            logger.debug(f"[FSM] idempotent allowed: {current} -> {new}")
            return True

        allowed = ALLOWED_TRANSITIONS.get(current, set())
        result = new in allowed

        logger.debug(
            f"[FSM] check transition: {current} -> {new} | allowed={result}"
        )

        return result

    def transition(self, current: UserState, new: UserState) -> UserState:
        """
        Safe transition. Raises error if invalid.
        """

        logger.info(f"[FSM] transition request: {current} -> {new}")

        if current == new:
            logger.info(f"[FSM] idempotent: {current} == {new}")
            return current

        if not self.can_transition(current, new):
            logger.error(
                f"[FSM] INVALID TRANSITION: {current} -> {new}"
            )
            raise ValueError(
                f"Invalid state transition: {current} -> {new}"
            )

        logger.info(f"[FSM] transition OK: {current} -> {new}")
        return new

    def force(self, new: UserState) -> UserState:
        logger.warning(f"[FSM] FORCE transition -> {new}")
        return new