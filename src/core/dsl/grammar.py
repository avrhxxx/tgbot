# src/core/dsl/grammar.py
# GROUP: core.dsl
# DESCRIPTION: DSL command registry (Stage 1 - deterministic compiler rules)

"""
SUPPORTED_COMMANDS defines all valid DSL operations in Stage 1.

RULE:
- DSL is closed-world
- every command must be explicitly declared here
- no implicit behavior
"""

SUPPORTED_COMMANDS = {
    # ENTITY LIFECYCLE
    "create_entity",
    "set_entity_type",

    # TYPE SYSTEM
    "create_type",

    # FIELD SYSTEM
    "create_field",
    "set_field",

    # RELATION SYSTEM
    "create_relation",
    "add_relation"
}