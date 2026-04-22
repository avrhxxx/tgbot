from datetime import datetime

from src.keyboards.keyboards import build_home_keyboard
from src.core.role_resolver import resolve_role


def render_home(state):
    """
    UNIFIED HOME SCREEN RENDERER
    (R3 / R4 / R5 handled via role context)
    """

    user_id = getattr(state, "user_id", None)

    game_nick = getattr(state, "game_nick", "Unknown Nick")

    first_name = getattr(state, "first_name", None)
    username = getattr(state, "telegram_username", None)

    display_name = first_name or username or "User"

    today_utc = datetime.utcnow().strftime("%Y-%m-%d")

    # =========================
    # 🧠 ROLE RESOLUTION (SOURCE OF TRUTH)
    # =========================
    role_ctx = resolve_role(user_id, state.role)
    role = role_ctx.effective_role

    text = (
        f"🏠 HOME PANEL\n\n"
        f"Welcome, {display_name}\n\n"
        f"Game Nick: {game_nick}\n"
        f"Role: {role}\n"
        f"Today (UTC): {today_utc}\n"
    )

    keyboard = build_home_keyboard(
        user_id=user_id,
        role=role
    )

    return {
        "text": text,
        "keyboard": keyboard
    }