from dataclasses import dataclass
from typing import Optional

from src.ui.definitions.screen_ids import ScreenID
from src.ui.definitions.role_ids import RoleID


@dataclass
class UIState:
    user_id: int
    screen: ScreenID
    role: RoleID

    # =========================
    # 🧠 ROLE CONTEXT (EXTENSION)
    # =========================
    demo_role: Optional[RoleID] = None

    # =========================
    # 👤 USER CONTEXT (OPTIONAL UI DATA)
    # =========================
    game_nick: Optional[str] = None
    first_name: Optional[str] = None
    telegram_username: Optional[str] = None