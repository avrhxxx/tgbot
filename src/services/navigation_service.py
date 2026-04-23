# src/services/navigation_service.py

class NavigationService:
    """
    MVP navigation layer (NO BUSINESS LOGIC YET)
    """

    def get_home_screen(self, role: str, demo_mode: bool) -> str:
        # ❌ usunięty demo_mode z UI
        return f"🏠 HOME SCREEN\nRole: {role}"

    def get_switch_roles_button(self):
        return {
            "text": "🔁 Switch Role",
            "callback_data": "demo.switch_role"
        }