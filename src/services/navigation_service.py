# src/services/navigation_service.py

class NavigationService:
    """
    MVP navigation layer (NO BUSINESS LOGIC YET)
    """

    def get_home_screen(self, role: str, demo_mode: bool) -> str:
        base = f"🏠 HOME SCREEN\nRole: {role}\n"

        if demo_mode:
            base += "\n🧪 DEMO MODE ACTIVE\n"

        return base

    def get_switch_roles_button(self):
        return {
            "text": "🔁 Switch Role (Demo)",
            "callback_data": "demo.switch_role"
        }