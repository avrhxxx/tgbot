from datetime import datetime

from src.keyboards.keyboards import home_keyboard


def render_home(state, role: str):
    """
    UNIFIED HOME SCREEN RENDERER
    role is already resolved upstream (router layer)
    """

    game_nick = getattr(state, "game_nick", "Unknown Nick")

    first_name = getattr(state, "first_name", None)
    username = getattr(state, "telegram_username", None)

    display_name = first_name or username or "User"

    today_utc = datetime.utcnow().strftime("%Y-%m-%d")

    text = (
        "🏠 HOME PANEL\n\n"
        f"Welcome, {display_name}\n\n"
        f"Game Nick: {game_nick}\n"
        f"Role: {role}\n"
        f"Today (UTC): {today_utc}\n"
    )

    return {
        "text": text,
        "keyboard": home_keyboard(role)
    }