# src/ui/models/ui_state.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class UIState:
    """
    Core UI state container.
    This will later control routing + screen rendering.
    """

    user_id: int
    role: Optional[str] = None

    current_screen: Optional[str] = None
    previous_screen: Optional[str] = None

    context: dict = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}