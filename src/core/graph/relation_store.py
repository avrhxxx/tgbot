from collections import defaultdict
from typing import Dict, Any, List, Tuple

from src.shared.logging import get_logger

logger = get_logger("RelationStore")


class RelationStore:
    """
    Simple in-memory graph structure:
    entity → relations → targets
    """

    def __init__(self):
        self._graph: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    def _key(self, entity_type: str, name: str) -> str:
        return f"{entity_type}:{name}"

    def add_relation(
        self,
        from_entity: Tuple[str, str],
        relation: str,
        to_entity: Tuple[str, str],
    ):
        src = self._key(*from_entity)
        dst = self._key(*to_entity)

        self._graph[src].append((relation, dst))

        logger.info(f"[GRAPH] {src} --{relation}--> {dst}")

    def get_relations(self, entity_type: str, name: str):
        return self._graph.get(self._key(entity_type, name), [])

    def dump(self) -> Dict[str, Any]:
        return dict(self._graph)