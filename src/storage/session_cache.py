# src/storage/session_cache.py

"""
Global in-memory session cache for Shadow Bot.

- TTL = 24h
- maxsize = RAM safety limit
"""

from typing import Any, Dict

from cachetools import TTLCache

# =========================
# SESSION DATA TYPE
# =========================
SessionData = Dict[str, Any]

SESSION_CACHE: TTLCache[str, SessionData] = TTLCache(
    maxsize=10_000,
    ttl=60 * 60 * 24  # 24h
)