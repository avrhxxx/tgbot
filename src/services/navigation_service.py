# src/services/navigation_service.py

from src.ui.screens.home_screen import render_home_screen
from src.ui.keyboards.home_keyboard import get_home_keyboard


class NavigationService:
    """
    UI Composer:
    builds complete view (text + keyboard)
    """

    def get_home_view(
        self,
        *,
        first_name: str,
        role: str,
        game_nick: str | None,
        is_demo: bool,
    ):
        return {
            "text": render_home_screen(first_name, role, game_nick),
            "keyboard": get_home_keyboard(is_demo),
        }