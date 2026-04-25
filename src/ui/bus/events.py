# =========================================
# GROUP: ui.bus
# FILE: events.py
# DESCRIPTION:
# UI events dispatched by buttons
# =========================================

from dataclasses import dataclass


@dataclass
class NavigateEvent:
    screen: str