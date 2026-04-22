from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Transition:
    from_screen: str
    action: str
    to_screen: str


class StateMachine:
    """
    Definiuje reguły przejść UI:
    screen + action => next screen
    """

    def __init__(self):
        self._transitions: Dict[str, Dict[str, str]] = {}

    def add_transition(self, from_screen: str, action: str, to_screen: str):
        if from_screen not in self._transitions:
            self._transitions[from_screen] = {}

        self._transitions[from_screen][action] = to_screen

    def get_next_screen(self, current_screen: str, action: str) -> Optional[str]:
        return self._transitions.get(current_screen, {}).get(action)

    def can_transition(self, current_screen: str, action: str) -> bool:
        return action in self._transitions.get(current_screen, {})