# src/services/navigation_service.py

from datetime import datetime


class NavigationService:
    """
    MVP navigation layer (UI rendering)
    """

    def get_home_screen(
        self,
        first_name: str,
        role: str,
        game_nick: str | None = None,
    ) -> str:
        now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

        game_nick_text = game_nick if game_nick else "Not set"

        return (
            f"Welcome, {first_name}\n\n"
            f"Game Nick: {game_nick_text}\n"
            f"Role: {role}\n"
            f"Today is {now_utc} UTC"
        )

    def get_switch_roles_button(self):
        return {
            "text": "🔁 Switch Role",
            "callback_data": "demo.switch_role"
        }