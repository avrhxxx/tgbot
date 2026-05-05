# GROUP: core.graph
# DESCRIPTION: In-memory graph store for entity relationships (MVP layer before Firestore)

from collections import defaultdict
from typing import Dict, Any, List

from src.shared.logging import get_logger
from src.core.graph.relation_types import RelationType

logger = get_logger("RelationStore")


class RelationStore:
    """
    Simple in-memory graph structure:
    entity → relations → targets
    """

    def __init__(self):
        # structure:
        # hero:Ares -> [("has_skill", "Fireball"), ("link_to_faction", "Olymp")]
        self._graph: Dict[str, List[tuple[str, str]]] = defaultdict(list)

    def _key(self, entity_type: str, name: str) -> str:
        return f"{entity_type}:{name}"

    # =========================
    # WRITE OPERATIONS
    # =========================

    def add_relation(
        self,
        from_entity: tuple[str, str],
        relation: RelationType,
        to_entity: tuple[str, str],
    ):
        src = self._key(*from_entity)
        dst = self._key(*to_entity)

        self._graph[src].append((relation.name, dst))

        logger.info(f"[GRAPH] {src} --{relation.name}--> {dst}")

    # =========================
    # READ OPERATIONS
    # =========================

    def get_relations(self, entity_type: str, name: str):
        key = self._key(entity_type, name)
        return self._graph.get(key, [])

    def dump(self) -> Dict[str, Any]:
        return dict(self._graph)