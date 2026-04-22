from src.keyboards.keyboards import home_keyboard
from src.core.state_store import state_store


def render_home_r3(state):
    """
    HOME R3 UI
    """

    user_id = getattr(state, "user_id", None)

    game_nick = getattr(state, "game_nick", "Unknown Nick")

    # REAL role from state
    real_role = getattr(state, "role", "R3")

    # DEMO OVERRIDE SAFE RESOLUTION
    role = state_store.get_effective_role(user_id, real_role) if user_id else real_role

    text = (
        f"🏠 HOME R3\n\n"
        f"User ID: {user_id}\n"
        f"Game Nick: {game_nick}\n"
        f"Role: {role}\n\n"
        f"Choose an option:"
    )

    return {
        "text": text,
        "keyboard": home_keyboard()
    }