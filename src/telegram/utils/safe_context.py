# =========================================
# GROUP: telegram.utils
# FILE: safe_context.py
# DESCRIPTION:
# Safe extraction layer for aiogram dialog events.
# Prevents union-attr / ErrorEvent crashes.
# =========================================

from typing import Optional
from aiogram.types import User
from aiogram_dialog import DialogManager


def get_user_safe(dialog_manager: DialogManager) -> Optional[User]:
    event = dialog_manager.event

    user = getattr(event, "from_user", None)

    if user is None:
        return None

    return user