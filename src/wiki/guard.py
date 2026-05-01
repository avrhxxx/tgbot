# src/wiki/guard.py
# GROUP: wiki
# DESCRIPTION: Soft game scope guard for AI Wiki Bot (Tiles Survive)

import logging

logger = logging.getLogger("wiki.guard")

GAME_KEYWORDS = {
    "tiles survive",
    "tilesurvive",
    "game",
    "strategy",
    "build",
    "upgrade",
    "units",
    "survivors",
    "base",
    "resources",
    "zombie",
}


def is_game_related(text: str) -> bool:
    """
    Checks if user question is related to Tiles Survive game.
    Soft classification (not strict NLP).
    """

    if not text:
        return False

    text_lower = text.lower()

    # hard anchor: game name
    if "tiles survive" in text_lower:
        return True

    # keyword match
    for kw in GAME_KEYWORDS:
        if kw in text_lower:
            return True

    return False


def build_redirect_message() -> str:
    """
    Message shown when user asks outside game scope.
    Soft redirect instead of hard block.
    """

    return (
        "I can only help with Tiles Survive! 🎮\n"
        "Ask me about strategies, upgrades, resources or gameplay tips."
    )