# src/storage/session_cache.py

from typing import Dict, Any

from cachetools import TTLCache

"""
Global in-memory session cache for Shadow Bot.

- TTL = 24h
- maxsize = limit RAM safety
"""

# =========================
# SESSION DATA TYPE
# =========================
SessionData = Dict[str, Any]

SESSION_CACHE: TTLCache[str, SessionData] = TTLCache(
    maxsize=10_000,
    ttl=60 * 60 * 24  # 24h
)