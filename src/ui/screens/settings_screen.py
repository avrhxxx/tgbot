# src/ui/screens/settings_screen.py


def render_settings_screen(app=None, user_id=None, callback=None):
    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            "Game profile settings:\n"
            "- Nick\n"
            "- Preferences\n"
        ),
        "keyboard": {
            "inline_keyboard": [
                [
                    {
                        "text": "🔙 Back",
                        "callback_data": "nav.home"
                    }
                ]
            ]
        }
    }