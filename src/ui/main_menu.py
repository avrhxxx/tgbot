# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main menu UI (single header line + fixed footer)
# =========================================

from datetime import datetime
from aiogram.types import User


WIDTH = 20


def line() -> str:
    return "─" * WIDTH


def build_title_line(title: str) -> str:
    """
    ─── MAIN MENU ───
    (centered inside fixed WIDTH line)
    """
    title = f" {title} "

    if len(title) >= WIDTH:
        return title[:WIDTH]

    total = WIDTH - len(title)
    left = total // 2
    right = total - left

    return "─" * left + title + "─" * right


def format_main_menu(user: User | None) -> str:
    name = user.first_name if user else "User"
    date = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        f"{build_title_line('MAIN MENU')}\n\n"
        f"Welcome, {name}\n"
        f"Date: {date}\n\n"
        "Have a nice day!\n\n"
        f"{line()}"
    )