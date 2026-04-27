# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main Menu UI renderer (premium dashboard style)
# =========================================

from datetime import datetime
from aiogram.types import User


def format_main_menu(user: User | None) -> str:
    # user name fallback chain
    name = "User"

    if user:
        name = user.first_name or user.full_name or "User"

    # date only (UTC)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        "╭──────────────────────────────╮\n"
        "           MAIN MENU\n"
        "╰──────────────────────────────╯\n\n"
        f"Welcome, {name}\n\n"
        f"Today is: {date_str}\n\n"
        "Have a nice day!\n\n"
        "──────────────────────────────"
    )