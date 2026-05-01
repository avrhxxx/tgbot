# src/wiki/search.py
# GROUP: wiki
# DESCRIPTION: Web knowledge layer (Reddit-first context builder for Tiles Survive wiki AI)

import logging

logger = logging.getLogger("wiki.search")


# =========================
# REDDIT CONTEXT LAYER (MVP)
# =========================

def fetch_reddit_context(query: str) -> str:
    """
    Mock Reddit-based context fetcher.
    In production: replace with Reddit API / RSS / scraping layer.

    Returns condensed "game knowledge context" for Gemini.
    """

    logger.info("Fetching Reddit context for query: %s", query)

    q = query.lower()

    # =========================
    # SIMULATED GAME KNOWLEDGE BASE
    # =========================

    if "early" in q or "start" in q:
        return """
Reddit community insights:
- Focus early on resource buildings first (food + materials)
- Upgrade command center ASAP to unlock systems
- Do NOT overinvest in defense early game
- Fast progression comes from balanced resource flow
"""

    if "upgrade" in q:
        return """
Reddit tips:
- Prioritize command center upgrades
- Upgrade production buildings before combat units
- Storage upgrades prevent resource loss during raids
"""

    if "strategy" in q or "best" in q:
        return """
Community meta strategy:
- Early game = economy > combat
- Mid game = balanced base + defense
- Late game = specialization of units
- Resource bottleneck is the main progression limiter
"""

    # fallback
    return """
No specific Reddit threads found.
General advice:
- Focus on resource production
- Upgrade core buildings first
- Avoid spreading upgrades too thin early game
"""