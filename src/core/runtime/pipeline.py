# src/core/runtime/pipeline.py
# GROUP: core.runtime
# DESCRIPTION: DSL execution pipeline (Stage 1 compiler runtime - FINAL CONTRACT)

from src.core.dsl.parser import DSLParser
from src.core.dsl.validator import DSLValidator
from src.core.runtime.executor import Executor

from src.core.state.entity_store import EntityStore

from src.domain.types.type_registry import TypeRegistry
from src.domain.fields.field_registry import FieldRegistry
from src.domain.relations.relation_registry import RelationRegistry

from src.shared.logging import get_logger
from src.shared.trace import ensure_trace_id

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
        logger.info(f"[trace={trace_id}] PIPELINE START")

        # =========================
        # 1. PARSE
        # =========================
        ast = self.parser.parse(text)

        # =========================
        # 2. VALIDATE (NON-BLOCKING)
        # =========================
        validated_ast = self.validator.validate(ast)

        # =========================
        # 3. EXECUTE
        # =========================
        exec_results = self.executor.execute(validated_ast)

        # =========================
        # 4. RESPONSE CONTRACT BUILD
        # =========================
        errors = [r for r in exec_results if r["status"] == "error"]
        ok = [r for r in exec_results if r["status"] == "ok"]

        response = {
            "status": "error" if errors else "ok",
            "trace_id": trace_id,
            "results": exec_results,
            "errors": errors,
            "meta": {
                "executed": len(ok),
                "failed": len(errors)
            }
        }

        logger.info(f"[trace={trace_id}] PIPELINE END")

        return response