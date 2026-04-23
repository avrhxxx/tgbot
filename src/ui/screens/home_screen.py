# src/ui/screens/home_screen.py

from src.ui.keyboards.home_keyboard import get_home_keyboard


def build_home_screen(app=None, user_id=None, callback=None, session=None) -> dict:
    """
    Screen renderer used by Screen Registry system.
    Pure function - no business logic, only presentation.
    """

    first_name = session.get("first_name", "User")
    role = session.get("role", "user")
    game_nick = session.get("game_nick")
    is_demo = app.is_demo() if app else False

    text = _build_text(first_name, role, game_nick)

    return {
        "text": text,
        "keyboard": get_home_keyboard(is_demo),
    }


def _build_text(first_name: str, role: str, game_nick: str | None) -> str:
    nick_line = (
        f"🎮 Game Nick: {game_nick}"
        if game_nick
        else "⚠️ No Game Nick set"
    )

    return (
        f"👋 Welcome {first_name}!\n\n"
        f"🧩 Role: {role}\n"
        f"{nick_line}\n\n"
        f"Select an option below:"
    )