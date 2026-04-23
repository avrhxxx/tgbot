# src/engine/session_engine.py

import logging
from dataclasses import dataclass
from typing import Optional, TypedDict, cast

from src.engine.state_machine import StateMachine, UserState
from src.storage.session_cache import SESSION_CACHE

logger = logging.getLogger("shadow.engine.session")


# =========================
# SESSION MODEL (STRICT)
# =========================
class SessionData(TypedDict):
    state: UserState
    game_nick: Optional[str]


# =========================
# SESSION ENGINE
# =========================
@dataclass
class SessionEngine:
    """
    Central user session manager.

    Uses:
    - cachetools TTLCache (in-memory global store)
    - state machine validation
    """

    state_machine: StateMachine

    # =========================
    # GET SESSION
    # =========================
    def get(self, user_id: str) -> SessionData:
        if user_id not in SESSION_CACHE:
            logger.info(f"[SESSION] init new session user={user_id}")

            SESSION_CACHE[user_id] = {
                "state": UserState.NEW,
                "game_nick": None,
            }

        session = cast(SessionData, SESSION_CACHE[user_id])

        logger.debug(
            f"[SESSION] get user={user_id} state={session['state']} nick={session['game_nick']}"
        )

        return session

    # =========================
    # STATE HANDLING
    # =========================
    def get_state(self, user_id: str) -> UserState:
        state = self.get(user_id)["state"]
        logger.debug(f"[SESSION] get_state user={user_id} state={state}")
        return state

    def set_state(self, user_id: str, new_state: UserState) -> None:
        session = self.get(user_id)
        current = session["state"]

        logger.info(
            f"[SESSION] state change request user={user_id} {current} -> {new_state}"
        )

        validated = self.state_machine.transition(current, new_state)

        session["state"] = validated

        logger.info(
            f"[SESSION] state updated user={user_id} -> {validated}"
        )

    # =========================
    # NICK HANDLING
    # =========================
    def get_nick(self, user_id: str) -> Optional[str]:
        nick = self.get(user_id)["game_nick"]
        logger.debug(f"[SESSION] get_nick user={user_id} nick={nick}")
        return nick

    def set_nick(self, user_id: str, nick: str) -> None:
        logger.info(f"[SESSION] set_nick user={user_id} nick={nick}")

        self.get(user_id)["game_nick"] = nick

    # =========================
    # RESET SESSION
    # =========================
    def clear(self, user_id: str) -> None:
        logger.warning(f"[SESSION] clear session user={user_id}")

        SESSION_CACHE.pop(user_id, None)