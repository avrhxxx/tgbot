# src/wiki/knowledge/source_registry.py

import json
from pathlib import Path
from typing import Set

FILE_PATH = Path("data/knowledge_sources.json")


class SourceRegistry:
    def __init__(self):
        self.sources: Set[str] = set()
        self._load()

    def _load(self):
        if FILE_PATH.exists():
            try:
                self.sources = set(json.loads(FILE_PATH.read_text()))
            except Exception:
                self.sources = set()

    def _save(self):
        FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        FILE_PATH.write_text(json.dumps(list(self.sources)))

    def is_known(self, url: str) -> bool:
        return url in self.sources

    def add(self, url: str):
        self.sources.add(url)
        self._save()