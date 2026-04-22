from src.core.registry import SCREEN_MAP

def resolve_screen(screen_id: str):
    return SCREEN_MAP.get(screen_id)