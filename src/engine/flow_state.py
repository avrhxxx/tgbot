# =========================================
# FILE: src/engine/flow_state.py
# DESCRIPTION:
# Simple in-memory flow state (n8n-style)
# =========================================

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

FLOW_STATE: Dict[int, Dict[str, Any]] = {}


def get_state(user_id: int) -> Dict[str, Any]:
    return FLOW_STATE.setdefault(user_id, {
        "flow": None,
        "step": None,
        "data": {}
    })


def set_flow(user_id: int, flow: str) -> None:
    state = get_state(user_id)
    state["flow"] = flow
    state["step"] = "start"
    state["data"] = {}
    logger.info(f"[FLOW] start flow={flow} user={user_id}")


def set_step(user_id: int, step: str) -> None:
    state = get_state(user_id)
    state["step"] = step
    logger.info(f"[FLOW] step={step} user={user_id}")


def set_data(user_id: int, key: str, value: Any) -> None:
    state = get_state(user_id)
    state["data"][key] = value


def get_data(user_id: int) -> Dict[str, Any]:
    state = get_state(user_id)

    # 🔥 FIX: avoid Any inference from .get()
    data = state.get("data")

    if data is None:
        data = {}
        state["data"] = data

    return data