from src.keyboards.keyboards import home_keyboard


def render_home_r3(state):
    """
    HOME R3 UI
    """

    return {
        "text": "🏠 HOME R3\n\nChoose an option:",
        "keyboard": home_keyboard()
    }