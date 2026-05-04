# src/ai/action_schema.py
# GROUP: ai
# DESCRIPTION: Core Action Schema - single source of truth for DSL → backend execution

from typing import Literal, Dict, Any, Optional, List


# =========================
# ENTITY TYPES
# =========================
EntityType = Literal[
    "hero",
    "skill",
    "item",
    "building",
    "research_tree",
    "research_node",
    "faction",
    "shop",
    "pve_entity",
    "game_event",
]


# =========================
# ACTION TYPES
# =========================
ActionType = Literal[
    "create_entity",
    "update_entity",
    "define_entity",
    "link_entity",
    "query_entity",
    "check_existence",
]


# =========================
# BASE ACTION
# =========================
class Action:
    action: ActionType
    type: Optional[EntityType]
    name: Optional[str]
    target: Optional[Dict[str, str]]
    field: Optional[str]
    value: Any
    context: Dict[str, Any]


# =========================
# EXAMPLES (REFERENCE ONLY)
# =========================

"""
CREATE:
{
  "action": "create_entity",
  "type": "hero",
  "name": "Tarzan"
}

UPDATE FIELD:
{
  "action": "update_entity",
  "type": "skill",
  "target": {
    "hero": "Tarzan",
    "skill": "Rage Slam"
  },
  "field": "damage",
  "value": 1200
}

DEFINE LORE:
{
  "action": "define_entity",
  "type": "hero",
  "name": "Tarzan",
  "field": "lore",
  "value": "..."
}

LINK:
{
  "action": "link_entity",
  "type": "skill",
  "target": {
    "parent_type": "hero",
    "parent_name": "Tarzan"
  }
}
"""