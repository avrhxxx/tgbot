# src/ui/screens/home_screen.py

from datetime import datetime, timezone


def render_home_screen(first_name: str, role: str, game_nick: str | None) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return (
        f"Welcome, {first_name}\n\n"
        f"Game Nick: {game_nick or 'not set'}\n"
        f"Role: {role}\n\n"
        f"Today is {now_utc} UTC"
    )