from src.keyboards.keyboards import home_keyboard


def render_home_r5(state):
    """
    HOME R5 UI
    """

    return {
        "text": "🏠 HOME R5\n\nChoose an option:",
        "keyboard": home_keyboard()
    }