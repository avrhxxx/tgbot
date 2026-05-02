# src/services/session_service.py
# GROUP: services
# DESCRIPTION: Lightweight per-user session memory (TTL-based) for conversational context

import logging
from cachetools import TTLCache
from typing import Dict, Any

logger = logging.getLogger("services.session")

# =========================
# SESSION STORAGE
# =========================
session_cache: TTLCache[int, Dict[str, Any]] = TTLCache(
    maxsize=10000,
    ttl=1800
)


def get_session(user_id: int) -> Dict[str, Any]:
    session = session_cache.get(user_id)

    if session is None:
        session = {
            "last_topic": None,
            "last_entities": [],
            "last_question": None,
        }
        session_cache[user_id] = session

    return session


def update_session(
    user_id: int,
    *,
    topic: str | None = None,
    entities: list[str] | None = None,
    question: str | None = None,
) -> None:

    session = get_session(user_id)

    if topic:
        session["last_topic"] = topic

    if entities:
        session["last_entities"] = entities

    if question:
        session["last_question"] = question

    session_cache[user_id] = session

    logger.debug("Session updated for user=%s", user_id)


def build_session_context(user_id: int) -> str:
    session = get_session(user_id)

    parts = []

    if session.get("last_topic"):
        parts.append(f"Last topic: {session['last_topic']}")

    if session.get("last_entities"):
        parts.append(f"Known entities: {', '.join(session['last_entities'])}")

    if session.get("last_question"):
        parts.append(f"Previous question: {session['last_question']}")

    if not parts:
        return ""

    return "PREVIOUS CONTEXT:\n" + "\n".join(parts)