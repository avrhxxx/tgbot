# GROUP: core.graph
# DESCRIPTION: Canonical relation types for Knowledge Graph layer

from dataclasses import dataclass


# =========================
# CORE RELATION TYPES
# =========================

@dataclass(frozen=True)
class RelationType:
    """
    Defines allowed semantic relationships in the system.
    """

    name: str


# Core gameplay relations
HAS_SKILL = RelationType("has_skill")
HAS_ITEM = RelationType("has_item")
HAS_BUILDING = RelationType("has_building")

LINK_TO_FACTION = RelationType("link_to_faction")
LINK_TO_TROOP_TYPE = RelationType("link_to_troop_type")

CONTAINS_NODE = RelationType("contains_node")
DEPENDS_ON = RelationType("depends_on")

# Generic fallback (for future AI expansion)
GENERIC_LINK = RelationType("generic_link")