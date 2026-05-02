# src/wiki/guard.py
# GROUP: wiki
# DESCRIPTION: Minimal soft guard (RAG-driven decision flow)

import logging

logger = logging.getLogger("wiki.guard")


OFFTOPIC_HINTS = [
    "cook",
    "recipe",
    "weather",
    "politics",
    "news",
    "football",
    "movie",
    "porn",
    "casino",
]


def is_game_related(text: str) -> bool:
    """
    Lightweight safety + off-topic filter.
    Does NOT decide game relevance anymore (RAG handles that).
    """

    if not text:
        return False

    text_lower = text.lower()

    # HARD OFF-TOPIC BLOCK ONLY
    for bad in OFFTOPIC_HINTS:
        if bad in text_lower:
            logger.info("Hard off-topic detected: %s", bad)
            return False

    # default: allow into RAG pipeline
    return True


def build_redirect_message() -> str:
    return (
        "I can only help with Tiles Survive! 🎮\n\n"
        "Ask about heroes, builds, upgrades or strategy."
    )