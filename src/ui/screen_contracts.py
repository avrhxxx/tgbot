# src/ui/screen_contracts.py
from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class ScreenDefinition:
    id: str
    handler: Callable[..., Dict[str, Any]]