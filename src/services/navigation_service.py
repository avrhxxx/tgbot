# src/services/navigation_service.py

from src.ui.screen_registry import ScreenRegistry


class NavigationService:
    """
    UI Composer layer (NEW ARCHITECTURE)

    Responsible ONLY for:
    - calling ScreenRegistry
    - passing context
    """

    def __init__(self, registry: ScreenRegistry):
        self.registry = registry

    def get_home_view(
        self,
        *,
        first_name: str,
        role: str,
        game_nick: str | None,
        is_demo: bool,
    ):
        return self.registry.render(
            "home",
            first_name=first_name,
            role=role,
            game_nick=game_nick,
            is_demo=is_demo,
        )

    def get_events_view(self, **context):
        return self.registry.render("events", **context)

    def get_settings_view(self, **context):
        return self.registry.render("settings", **context)