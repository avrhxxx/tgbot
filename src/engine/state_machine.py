from dataclasses import dataclass, field
from typing import Any, Dict


# =========================
# UI STATE OBJECT
# =========================

@dataclass
class UIState:
    screen: str
    role: str
    data: Dict[str, Any] = field(default_factory=dict)


# =========================
# STATE MACHINE
# =========================

class StateMachine:
    def __init__(self):
        self._state: UIState | None = None

    # -------------------------
    # GET CURRENT STATE
    # -------------------------
    def get_state(self) -> UIState | None:
        return self._state

    # -------------------------
    # SET INITIAL STATE
    # -------------------------
    def init_state(self, screen: str = "home_r3", role: str = "R3"):
        self._state = UIState(
            screen=screen,
            role=role,
            data={}
        )

        return self._state

    # -------------------------
    # UPDATE STATE
    # -------------------------
    def update_state(
        self,
        screen: str | None = None,
        role: str | None = None,
        data: Dict[str, Any] | None = None,
    ) -> UIState:
        if self._state is None:
            self.init_state()

        if screen:
            self._state.screen = screen

        if role:
            self._state.role = role

        if data:
            self._state.data.update(data)

        return self._state

    # -------------------------
    # RESET STATE
    # -------------------------
    def reset(self):
        self._state = None