# src/wiki/ingestion/source_registry.py
# GROUP: wiki.ingestion
# DESCRIPTION: Prevents duplicate ingestion of the same sources

import time
from typing import Set


class SourceRegistry:
    """
    In-memory deduplication layer.
    Prevents re-processing same URLs during runtime.
    """

    def __init__(self):
        self._seen_urls: Set[str] = set()
        self._created_at = time.time()

    def is_seen(self, url: str) -> bool:
        return url in self._seen_urls

    def mark_seen(self, url: str) -> None:
        self._seen_urls.add(url)

    def reset(self) -> None:
        self._seen_urls.clear()
        self._created_at = time.time()