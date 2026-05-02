# src/wiki/guard.py
# GROUP: wiki
# DESCRIPTION: Minimal scope guard (only hard off-topic detection)

import logging

logger = logging.getLogger("wiki.guard")

GAME_ANCHOR = "tiles survive"


def is_game_related(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()

    # ONLY hard block outside domain
    return GAME_ANCHOR in text_lower


def build_redirect_message() -> str:
    return (
        "I can only help with *Tiles Survive!* 🎮\n\n"
        "Ask me about gameplay, strategies, heroes or upgrades."
    )