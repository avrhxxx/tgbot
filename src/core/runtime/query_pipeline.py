# ============================================================
# FILE: src/core/runtime/query_pipeline.py
# PURPOSE: AI Read Pipeline (Graph + Semantic + AI Coach)
# FIX: Stage 1 stable runtime (no missing deps)
# ============================================================

from src.core.graph.query_engine import QueryEngine
from src.core.graph.relation_store import RelationStore

from src.ai.context_builder import ContextBuilder

from src.shared.logging import get_logger
from src.shared.trace import ensure_trace_id

logger = get_logger("query_pipeline")


class QueryPipeline:
    """
    STABLE AI READ PIPELINE (Stage 1 safe version)

    FLOW:
    USER TEXT → SIMPLE QUERY → GRAPH → CONTEXT → RESPONSE
    """

    def __init__(self):

        # -------------------------
        # GRAPH LAYER (FIXED)
        # -------------------------
        self.graph = QueryEngine(RelationStore())

        # -------------------------
        # CONTEXT BUILDER
        # -------------------------
        self.context_builder = ContextBuilder()

    # ============================================================
    # SIMPLE QUERY PARSING (TEMPORARY REPLACEMENT FOR QueryParser)
    # ============================================================
    def _parse_query(self, text: str) -> dict:

        text_lower = text.lower()

        return {
            "raw": text,
            "intent": "ENTITY_QUERY",
            "entity": text_lower.replace(" ", "_"),
            "filters": []
        }

    # ============================================================
    # MAIN HANDLER
    # ============================================================
    def handle(self, text: str, user_id: str, session_id: str):

        trace_id = ensure_trace_id()

        logger.info("QUERY_PIPELINE_START")

        # =========================
        # 1. PARSE (SAFE FALLBACK)
        # =========================
        query = self._parse_query(text)

        logger.info(f"QUERY_PARSED: {query['entity']}")

        # =========================
        # 2. GRAPH RETRIEVAL (FIXED API)
        # =========================
        graph_result = self.graph.get_by_source(query["entity"])

        logger.info(f"GRAPH_FETCHED: {len(graph_result)} relations")

        # =========================
        # 3. CONTEXT BUILD (SAFE CALL)
        # =========================
        try:
            context = self.context_builder.build(graph_result)
        except Exception as e:
            logger.warning(f"CONTEXT_BUILDER_FALLBACK: {e}")
            context = {
                "query": query,
                "graph_result": graph_result
            }

        # =========================
        # 4. RESPONSE (NO AI DEPENDENCY YET)
        # =========================
        response = {
            "entity": query["entity"],
            "data": context,
            "trace_id": trace_id
        }

        logger.info("QUERY_PIPELINE_END")

        return response