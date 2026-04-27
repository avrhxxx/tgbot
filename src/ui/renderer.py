# =========================================
# FILE: src/ui/renderer.py
# DESCRIPTION:
# Pure UI renderer (NO logic, only Telegram formatting)
# =========================================

from aiogram.types import InlineKeyboardMarkup


def render_message(text: str) -> str:
    return text or "⚠️ Empty response"


def render_edit_payload(data: dict) -> tuple[str, InlineKeyboardMarkup | None]:
    """
    n8n returns:
    {
        "text": "...",
        "keyboard": InlineKeyboardMarkup (or dict)
    }
    """

    text = data.get("text", "No response from n8n")
    keyboard = data.get("keyboard")

    return text, keyboard