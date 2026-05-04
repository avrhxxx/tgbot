# src/google/docs/templates/hero.py
# GROUP: google.docs.templates
# DESCRIPTION: Hero document template generator

def build_hero_template(name: str) -> str:
    return f"""
=====================================
HERO DOCUMENT
=====================================

NAME:
{name}

=====================================
BASIC INFO
=====================================
- Role:
- Type:
- Difficulty:
- Region:

=====================================
SKILLS
=====================================

[PASSIVE]
- Name:
- Description:
- Scaling:
- Notes:

[SKILL 1]
- Name:
- Type (auto_attack / passive / combat / talent):
- Description:
- Cooldown:
- Stats:

[SKILL 2]
- Name:
- Type:
- Description:
- Cooldown:
- Stats:

[SKILL 3]
- Name:
- Type:
- Description:
- Cooldown:
- Stats:

[ULTIMATE]
- Name:
- Description:
- Cooldown:
- Stats:

=====================================
LORE
=====================================
- Background:

=====================================
GAMEPLAY NOTES
=====================================
- Strengths:
- Weaknesses:
- Combos:

=====================================
END OF DOCUMENT
=====================================
"""