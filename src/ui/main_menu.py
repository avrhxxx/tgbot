# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main menu UI (dynamic header + fixed footer line)
# =========================================

from datetime import datetime
from aiogram.types import User


WIDTH = 20  # dolna linia (stała)


def bottom_line() -> str:
    return "─" * WIDTH


def build_header(title: str) -> str:
    """
    Tworzy linię: ───── MAIN MENU ─────
    z wycentrowanym tytułem.
    """
    title = f" {title} "

    if len(title) >= WIDTH:
        return title[:WIDTH]

    total_space = WIDTH - len(title)
    left = total_space // 2
    right = total_space - left

    return "─" * left + title + "─" * right


def format_main_menu(user: User | None) -> str:
    name = user.first_name if user else "User"
    date = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        f"{build_header('MAIN MENU')}\n\n"
        f"Welcome, {name}\n"
        f"Date: {date}\n\n"
        "Have a nice day!\n\n"
        f"{bottom_line()}"
    )