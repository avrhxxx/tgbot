# src/storage/session_cache.py

from cachetools import TTLCache

"""
Global in-memory session cache for Shadow Bot.

- TTL = 24h (możesz zmienić)
- maxsize = limit RAM safety
"""

SESSION_CACHE = TTLCache(
    maxsize=10_000,
    ttl=60 * 60 * 24  # 24h
)