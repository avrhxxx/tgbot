# =========================================
# FILE: src/engine/flow_state.py
# DESCRIPTION:
# Simple in-memory flow state (n8n-style replacement for aiogram-dialog FSM)
# =========================================

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# user_id -> state
FLOW_STATE: Dict[int, Dict[str, Any]] = {}


def get_state(user_id: int) -> Dict[str, Any]:
    return FLOW_STATE.setdefault(user_id, {
        "flow": None,
        "step": None,
        "data": {}
    })


def set_flow(user_id: int, flow: str):
    state = get_state(user_id)
    state["flow"] = flow
    state["step"] = "start"
    state["data"] = {}
    logger.info(f"[FLOW] start flow={flow} user={user_id}")


def set_step(user_id: int, step: str):
    state = get_state(user_id)
    state["step"] = step
    logger.info(f"[FLOW] step={step} user={user_id}")


def set_data(user_id: int, key: str, value: Any):
    state = get_state(user_id)
    state["data"][key] = value


def get_data(user_id: int) -> Dict[str, Any]:
    return get_state(user_id)["data"]