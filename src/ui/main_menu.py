# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main menu UI (dynamic centering + compact separators)
# =========================================

from datetime import datetime
from aiogram.types import User


WIDTH = 20  # kontrola długości UI (krótsze = bardziej compact)


def center(text: str, width: int = WIDTH) -> str:
    padding = max(0, (width - len(text)) // 2)
    return " " * padding + text


def line(char: str = "─") -> str:
    return char * WIDTH


def format_main_menu(user: User | None) -> str:
    name = user.first_name if user else "User"
    date = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        f"╭{line()}╮\n"
        f"{center('MAIN MENU')}\n"
        f"╰{line()}╯\n\n"
        f"Welcome, {name}\n"
        f"Date: {date}\n\n"
        "Have a nice day!\n\n"
        f"{line()}"
    )