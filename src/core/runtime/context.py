# ============================================================
# FILE: src/core/runtime/context.py
# PURPOSE: Execution context (trace_id, role, metadata)
# ============================================================

class ExecutionContext:
    def __init__(self, user_id: str, is_admin: bool, trace_id: str):
        self.user_id = user_id
        self.is_admin = is_admin
        self.trace_id = trace_id