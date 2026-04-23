# src/services/user_service.py

from typing import TypedDict, Optional


class UserData(TypedDict):
    role: str
    game_nick: Optional[str]


class UserService:
    """
    MVP user service (NO GOOGLE YET)
    """

    def __init__(self):
        # user_id -> user data
        self.users: dict[str, UserData] = {}

    # =========================
    # INTERNAL USER MODEL
    # =========================
    def _ensure_user(self, user_id: str) -> None:
        if user_id not in self.users:
            self.users[user_id] = {
                "role": "R3",
                "game_nick": None,
            }

    # =========================
    # ROLE SYSTEM
    # =========================
    def get_role(self, user_id: str) -> str:
        self._ensure_user(user_id)
        return self.users[user_id]["role"]

    def set_role(self, user_id: str, role: str) -> None:
        self._ensure_user(user_id)
        self.users[user_id]["role"] = role

    def cycle_role(self, current: str) -> str:
        order = ["R3", "R4", "R5"]
        idx = order.index(current)
        return order[(idx + 1) % len(order)]

    # =========================
    # GAME NICK SYSTEM (ONBOARDING)
    # =========================
    def get_game_nick(self, user_id: str) -> Optional[str]:
        self._ensure_user(user_id)
        return self.users[user_id]["game_nick"]

    def set_game_nick(self, user_id: str, nick: str) -> None:
        self._ensure_user(user_id)
        self.users[user_id]["game_nick"] = nick

    def has_game_nick(self, user_id: str) -> bool:
        self._ensure_user(user_id)
        return self.users[user_id]["game_nick"] is not None