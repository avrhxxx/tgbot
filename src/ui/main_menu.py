# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main menu UI (dynamic centering + compact separators)
# =========================================

from datetime import datetime
from aiogram.types import User


WIDTH = 20  # szerokość UI (kontener)

def line(char: str = "─") -> str:
    return char * WIDTH


def center(text: str, width: int = WIDTH) -> str:
    """
    Prawdziwe centrowanie tekstu w ramach WIDTH.
    Jeśli tekst jest dłuższy → przycina.
    """
    text = str(text)

    if len(text) >= width:
        return text[:width]

    padding_left = (width - len(text)) // 2
    padding_right = width - len(text) - padding_left

    return " " * padding_left + text + " " * padding_right


def format_main_menu(user: User | None) -> str:
    name = user.first_name if user else "User"
    date = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        f"╭{line()}╮\n"
        f"│{center('MAIN MENU')}│\n"
        f"╰{line()}╯\n\n"
        f"Welcome, {name}\n"
        f"Date: {date}\n\n"
        "Have a nice day!\n\n"
        f"{line()}"
    )