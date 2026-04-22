from src.keyboards.keyboards import home_keyboard


def render_home_r3(state):
    """
    HOME R3 UI
    """

    user_id = getattr(state, "user_id", None)
    game_nick = getattr(state, "game_nick", "Unknown Nick")
    role = getattr(state, "role", "R3")

    text = (
        f"🏠 HOME R3\n\n"
        f"User ID: {user_id}\n"
        f"Game Nick: {game_nick}\n"
        f"Role: {role}\n\n"
        f"Choose an option:"
    )

    return {
        "text": text,
        "keyboard": home_keyboard(user_id=user_id)
    }