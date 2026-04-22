from enum import Enum

class Action(str, Enum):
    GO_HOME = "go_home"
    OPEN_EVENT = "open_event"
    BACK = "back"