from dataclasses import dataclass

@dataclass
class UIState:
    user_id: int
    screen: str
    role: str  # R3 / R4 / R5