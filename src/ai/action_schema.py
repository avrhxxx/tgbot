# src/ai/action_schema.py
# GROUP: ai
# DESCRIPTION: Runtime Action Contract for Natural DSL → Backend Execution

from typing import Dict, Any, Literal


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
    "troop_type",
    "stat",
]


# =========================
# ACTION TYPES
# =========================
ActionType = Literal[
    "create",
    "update",
    "define",
    "add",
    "link",
    "show",
    "exists",
    "missing_fields",
    "schema",
]


# =========================
# NORMALIZATION → AST ALIGNMENT
# =========================
def normalize_action(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    DSL parser output → Command AST compatible format
    """

    return {
        "action": raw.get("action"),
        "entity": raw.get("entity"),
        "target": raw.get("target"),
        "attr": raw.get("attr"),
        "value": raw.get("value"),
        "relation": raw.get("relation"),
        "context": raw.get("context", {}),
    }


# =========================
# DSL RULES (REFERENCE ONLY)
# =========================
"""
SYNTAX RULES:

1. Names ALWAYS in quotes:
   "Tarzan", "Rage Slam"

2. Values WITHOUT quotes:
   1200, SSR, 8

3. One command = one operation

4. Nested relations use "of":
   update skill "Rage Slam" of hero "Tarzan" attr damage 1200

5. Linking:
   add skill "X" to hero "Y"
"""


# =========================
# EXAMPLES
# =========================
EXAMPLES = {

    "create": 'create hero "Tarzan"',

    "update_field": 'update hero "Tarzan" attr tier SSR',

    "update_nested": 'update skill "Rage Slam" of hero "Tarzan" attr damage 1200',

    "define_lore": 'define hero "Tarzan" lore "blood rage fighter..."',

    "link": 'link hero "Tarzan" to faction "Stalwart"',

    "add_relation": 'add skill "Rage Slam" to hero "Tarzan"',

    "query": 'show hero "Tarzan"',

    "validate": 'exists hero "Tarzan"',
}