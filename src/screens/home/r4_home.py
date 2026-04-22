from src.keyboards.keyboards import home_keyboard


def render_home_r4(state):
    """
    HOME R4 UI
    """

    return {
        "text": "🏠 HOME R4\n\nChoose an option:",
        "keyboard": home_keyboard()
    }