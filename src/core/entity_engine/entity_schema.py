# src/core/entity_engine/entity_schema.py
# GROUP: core.entity_engine
# DESCRIPTION: Unified game ontology schema (single source of truth for entity structure)

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


# =========================
# BASE SCHEMA MODEL
# =========================

@dataclass
class FieldSchema:
    type: str
    default: Any = None
    mutable: bool = True
    min_value: Optional[int] = None
    max_value: Optional[int] = None


@dataclass
class EntitySchema:
    name: str
    fields: Dict[str, FieldSchema]
    relations: List[str]


# =========================
# HERO SCHEMA
# =========================

HERO_SCHEMA = EntitySchema(
    name="hero",
    fields={
        "attack": FieldSchema(type="int", default=0, min_value=0),
        "defense": FieldSchema(type="int", default=0, min_value=0),
        "health": FieldSchema(type="int", default=100, min_value=1),
        "tier": FieldSchema(type="str", default="R"),
        "star_level": FieldSchema(type="int", default=1, min_value=1, max_value=10),
        "march_capacity": FieldSchema(type="int", default=0, min_value=0),
        "lore": FieldSchema(type="str", default=""),
    },
    relations=[
        "skills",
        "faction",
        "equipment"
    ]
)


# =========================
# SKILL SCHEMA
# =========================

SKILL_SCHEMA = EntitySchema(
    name="skill",
    fields={
        "damage": FieldSchema(type="int", default=0, min_value=0),
        "cooldown": FieldSchema(type="int", default=0, min_value=0),
        "level": FieldSchema(type="int", default=1, min_value=1, max_value=100),
        "description": FieldSchema(type="str", default=""),
    },
    relations=[
        "hero"
    ]
)


# =========================
# ITEM SCHEMA
# =========================

ITEM_SCHEMA = EntitySchema(
    name="item",
    fields={
        "rarity": FieldSchema(type="str", default="common"),
        "value": FieldSchema(type="int", default=0, min_value=0),
        "effect": FieldSchema(type="str", default=""),
    },
    relations=[
        "hero"
    ]
)


# =========================
# BUILDING SCHEMA
# =========================

BUILDING_SCHEMA = EntitySchema(
    name="building",
    fields={
        "level": FieldSchema(type="int", default=1, min_value=1),
        "production": FieldSchema(type="int", default=0),
        "capacity": FieldSchema(type="int", default=0),
    },
    relations=[]
)


# =========================
# RESEARCH NODE SCHEMA
# =========================

RESEARCH_NODE_SCHEMA = EntitySchema(
    name="research_node",
    fields={
        "cost": FieldSchema(type="int", default=0),
        "time": FieldSchema(type="int", default=0),
        "level": FieldSchema(type="int", default=1),
    },
    relations=[
        "research_tree"
    ]
)


# =========================
# REGISTRY (SINGLE ACCESS POINT)
# =========================

ENTITY_SCHEMAS = {
    "hero": HERO_SCHEMA,
    "skill": SKILL_SCHEMA,
    "item": ITEM_SCHEMA,
    "building": BUILDING_SCHEMA,
    "research_node": RESEARCH_NODE_SCHEMA,
}