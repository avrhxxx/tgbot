from datetime import datetime
from src.keyboards.keyboards import home_keyboard


def render_home_r4(state):
    """
    HOME R4 UI
    """

    user_id = getattr(state, "user_id", None)
    game_nick = getattr(state, "game_nick", "Unknown Nick")
    first_name = getattr(state, "first_name", None)
    username = getattr(state, "telegram_username", None)

    display_name = first_name or username or "User"
    today_utc = datetime.utcnow().strftime("%Y-%m-%d")

    text = (
        f"🏠 Home Panel\n\n"
        f"Welcome, {display_name}\n\n"
        f"Game Nick: {game_nick}\n"
        f"Role: R4\n"
        f"Today is (UTC): {today_utc}\n\n"
        f"Select an option:"
    )

    return {
        "text": text,
        "keyboard": home_keyboard(user_id=user_id)
    }