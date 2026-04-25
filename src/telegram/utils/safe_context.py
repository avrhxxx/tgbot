# =========================================
# GROUP: telegram.utils
# FILE: safe_context.py
# DESCRIPTION:
# Safe access layer for aiogram-dialog event/user
# fixes union-type mypy crashes
# =========================================

from typing import Optional, Any

from aiogram.types import User


def get_event_user(dialog_manager) -> Optional[User]:
    event = getattr(dialog_manager, "event", None)

    if not event:
        return None

    user = getattr(event, "from_user", None)

    return user if isinstance(user, User) else None


def get_user_safe(dialog_manager) -> Optional[User]:
    """
    Priority:
    1. middleware user
    2. event.from_user (safe)
    """
    user = dialog_manager.middleware_data.get("user")

    if user:
        return user

    return get_event_user(dialog_manager)
