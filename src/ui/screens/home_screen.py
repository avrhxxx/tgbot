# src/ui/screens/home_screen.py

from src.services.navigation_service import NavigationService


def render_home_screen(first_name: str, role: str, game_nick: str | None, app=None, user_id=None, callback=None):
    nav = app.services.get("nav")

    return nav.get_home_view(
        first_name=first_name,
        role=role,
        game_nick=game_nick,
        is_demo=app.is_demo(),
    )