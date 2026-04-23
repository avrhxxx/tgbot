# src/ui/screens/home_screen.py

from src.ui.keyboards.home_keyboard import get_home_keyboard


def build_home_screen(data: dict) -> dict:
    """
    Screen renderer used by Screen Registry system.
    Pure function - no dependencies on services or app context.
    """

    first_name = data["first_name"]
    role = data["role"]
    game_nick = data.get("game_nick")
    is_demo = data.get("is_demo", False)

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