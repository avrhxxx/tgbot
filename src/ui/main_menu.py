# =========================================
# FILE: src/ui/main_menu.py
# DESCRIPTION:
# Main menu UI (plain text version)
# =========================================

from datetime import datetime
from aiogram.types import User


def format_main_menu(user: User | None) -> str:
    name = user.first_name if user else "User"
    date = datetime.utcnow().strftime("%Y-%m-%d")

    return (
        "MAIN MENU\n\n"
        f"Welcome, {name}\n"
        f"Date: {date}\n\n"
        "Have a nice day!"
    )