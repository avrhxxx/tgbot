from datetime import datetime
from src.keyboards.keyboards import home_keyboard


def render_home_r3(state):
    """
    HOME R3 UI
    """

    user_id = getattr(state, "user_id", None)
    game_nick = getattr(state, "game_nick", "Unknown Nick")
    role = getattr(state, "role", "R3")

    first_name = getattr(state, "first_name", None)
    username = getattr(state, "telegram_username", None)

    display_name = first_name or username or "User"

    today_utc = datetime.utcnow().strftime("%Y-%m-%d")

    text = (
        f"🏠 HOME PANEL\n\n"
        f"Welcome, {display_name}\n\n"
        f"Game Nick: {game_nick}\n"
        f"Role: {role}\n"
        f"Today (UTC): {today_utc}\n\n"
        f"Navigation ready."
    )

    return {
        "text": text,
        "keyboard": home_keyboard(user_id=user_id)
    }