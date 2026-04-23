from dataclasses import dataclass
from enum import Enum


# =========================
# ACTION DOMAINS
# =========================
class ActionDomain(str, Enum):
    NAV = "nav"
    EVENT = "event"
    SETTINGS = "settings"
    ROLE = "role"
    SYSTEM = "system"


# =========================
# ACTION TYPES (LOGIC LEVEL)
# =========================
class ActionType(str, Enum):
    GO = "go"
    OPEN = "open"
    JOIN = "join"
    LEAVE = "leave"
    CREATE = "create"
    SWITCH = "switch"
    CHANGE = "change"
    BACK = "back"


# =========================
# CALLBACK FORMAT
# =========================
# domain:type:payload
#
# examples:
# nav:go:home
# event:open:123
# event:join:456
# settings:change:game_nick
# role:switch:
# system:back:
# =========================


@dataclass(frozen=True)
class Action:
    domain: ActionDomain
    type: ActionType
    payload: str | None = None

    def encode(self) -> str:
        """
        Convert Action → callback_data string
        """
        parts = [
            self.domain.value,
            self.type.value,
            self.payload or "",
        ]
        return ":".join(parts)

    @staticmethod
    def decode(data: str) -> "Action":
        """
        Convert callback_data → Action
        """
        parts = data.split(":")
        domain = ActionDomain(parts[0])
        action_type = ActionType(parts[1])
        payload = parts[2] if len(parts) > 2 else None

        return Action(domain=domain, type=action_type, payload=payload)


# =========================
# HELPERS (FACTORY STYLE)
# =========================

def nav_home() -> Action:
    return Action(ActionDomain.NAV, ActionType.GO, "home")


def nav_events() -> Action:
    return Action(ActionDomain.NAV, ActionType.GO, "events")


def nav_settings() -> Action:
    return Action(ActionDomain.NAV, ActionType.GO, "settings")


def event_open(event_id: str) -> Action:
    return Action(ActionDomain.EVENT, ActionType.OPEN, event_id)


def event_join(event_id: str) -> Action:
    return Action(ActionDomain.EVENT, ActionType.JOIN, event_id)


def event_leave(event_id: str) -> Action:
    return Action(ActionDomain.EVENT, ActionType.LEAVE, event_id)


def role_switch() -> Action:
    return Action(ActionDomain.ROLE, ActionType.SWITCH)


def settings_change(field: str) -> Action:
    return Action(ActionDomain.SETTINGS, ActionType.CHANGE, field)