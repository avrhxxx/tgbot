# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: DSL execution pipeline (Stage 1 compiler runtime - FINAL CONTRACT + Observability v2)

from src.core.dsl.parser import DSLParser
from src.core.dsl.validator import DSLValidator
from src.core.runtime.executor import Executor

from src.core.state.entity_store import EntityStore

from src.domain.types.type_registry import TypeRegistry
from src.domain.fields.field_registry import FieldRegistry
from src.domain.relations.relation_registry import RelationRegistry

from src.shared.logging import (
    get_logger,
    timed_stage,
    log_action
)
from src.shared.trace import ensure_trace_id

import time

logger = get_logger("pipeline")


class Pipeline:
    """
    Stage 1 Execution Pipeline

    FLOW:
    DSL TEXT → PARSE → VALIDATE → EXECUTE → RESPONSE CONTRACT
    """

    def __init__(self):

        # -----------------------------
        # DSL CORE
        # -----------------------------
        self.parser = DSLParser()

        # -----------------------------
        # REGISTRIES
        # -----------------------------
        self.type_registry = TypeRegistry()
        self.field_registry = FieldRegistry()
        self.relation_registry = RelationRegistry()

        self.validator = DSLValidator(
            type_registry=self.type_registry,
            field_registry=self.field_registry,
            relation_registry=self.relation_registry
        )

        # -----------------------------
        # GRAPH STATE
        # -----------------------------
        self.entity_store = EntityStore()

        self.executor = Executor(
            entity_store=self.entity_store
        )

    def handle(self, text: str):
        return self.run(text)

    def run(self, text: str):

        trace_id = ensure_trace_id()
        start_total = time.time()

        logger.info("PIPELINE START")

        # =========================
        # 1. PARSE
        # =========================
        with timed_stage(logger, "PARSE"):
            ast = self.parser.parse(text)

        # =========================
        # 2. VALIDATE
        # =========================
        with timed_stage(logger, "VALIDATE"):
            validated_ast = self.validator.validate(ast)

        # =========================
        # 3. EXECUTE
        # =========================
        with timed_stage(logger, "EXECUTE"):
            exec_results = self.executor.execute(validated_ast)

            # 🔥 KLUCZOWE: logowanie faktycznych operacji
            for r in exec_results:
                if r["status"] == "ok":
                    log_action(
                        logger,
                        r.get("type", "unknown"),
                        r.get("entity") or r.get("value") or ""
                    )
                else:
                    log_action(logger, "ERROR", str(r))

        # =========================
        # 4. RESPONSE CONTRACT BUILD
        # =========================
        errors = [r for r in exec_results if r["status"] == "error"]
        ok = [r for r in exec_results if r["status"] == "ok"]

        total_ms = int((time.time() - start_total) * 1000)

        response = {
            "status": "error" if errors else "ok",
            "trace_id": trace_id,
            "results": exec_results,
            "errors": errors,
            "meta": {
                "executed": len(ok),
                "failed": len(errors),
                "duration_ms": total_ms
            }
        }

        logger.info(f"PIPELINE END ({response['status']} | {total_ms}ms)")

        return response