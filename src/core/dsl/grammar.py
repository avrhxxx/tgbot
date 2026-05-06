# ============================================================
# FILE: src/core/dsl/grammar.py
# PURPOSE: DSL grammar definition (Stage 1 minimal)
# ============================================================

# NOTE:
# This file defines allowed DSL commands and structure.
# Used by validator (NOT parser directly).

SUPPORTED_COMMANDS = {
    "create_entity",
    "set_field",
    "add_relation",
}