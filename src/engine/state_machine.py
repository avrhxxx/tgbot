# src/engine/state_machine.py

from enum import Enum
from dataclasses import dataclass


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
        UserState.AWAITING_NICK,  # idempotent safety
    },

    UserState.HOME: {
        UserState.IN_EVENT,
        UserState.AWAITING_NICK,  # FIX: onboarding fallback
        UserState.HOME,           # idempotent safety
    },

    UserState.IN_EVENT: {
        UserState.HOME,
        UserState.IN_SQUAD,
        UserState.IN_EVENT,       # idempotent safety
    },

    UserState.IN_SQUAD: {
        UserState.HOME,
        UserState.IN_SQUAD,       # idempotent safety
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
        # hard safety: allow idempotent transitions globally
        if current == new:
            return True

        allowed = ALLOWED_TRANSITIONS.get(current, set())
        return new in allowed

    def transition(self, current: UserState, new: UserState) -> UserState:
        """
        Safe transition. Raises error if invalid.
        """

        # idempotent protection (VERY IMPORTANT for UI flows)
        if current == new:
            return current

        if not self.can_transition(current, new):
            raise ValueError(
                f"Invalid state transition: {current} -> {new}"
            )

        return new

    def force(self, new: UserState) -> UserState:
        """
        Bypass rules (admin/system usage only).
        """
        return new