# src/services/user_service.py


class UserService:
    """
    MVP user service (NO GOOGLE YET)
    """

    def __init__(self):
        self.users = {}  # user_id -> role

    def get_role(self, user_id: str) -> str:
        return self.users.get(user_id, "R3")

    def set_role(self, user_id: str, role: str):
        self.users[user_id] = role

    def cycle_role(self, current: str) -> str:
        order = ["R3", "R4", "R5"]

        idx = order.index(current)
        return order[(idx + 1) % len(order)]