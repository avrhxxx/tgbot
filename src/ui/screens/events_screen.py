# src/ui/screens/events_screen.py

def render_events_screen(app=None, user_id=None, callback=None):
    return {
        "text": (
            "📅 EVENTS\n\n"
            "Here you will see all available events.\n\n"
            "Status: MVP placeholder"
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