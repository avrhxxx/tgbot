# =========================================
# GROUP: utils
# FILE: access.py
# DESCRIPTION:
# Simple role-based access control (MVP).
# =========================================

from src.config.config import load_config


def get_config():
    return load_config()


def is_admin(user_id: int) -> bool:
    config = get_config()
    return user_id in config.access.admin_ids


def is_mod(user_id: int) -> bool:
    config = get_config()
    return user_id in config.access.mod_ids


def can_use_panel(user_id: int) -> bool:
    return is_admin(user_id) or is_mod(user_id)


def get_chat_ids() -> list[int]:
    config = get_config()
    return config.access.chat_ids