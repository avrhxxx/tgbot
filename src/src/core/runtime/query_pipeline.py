# ============================================================
# FILE: src/core/runtime/query_pipeline.py
# PURPOSE: AI Read Pipeline (Graph + Semantic + AI Coach)
# ============================================================

from src.semantic.query_parser import QueryParser
from src.core.graph.query_engine import QueryEngine
from src.ai.context_builder import ContextBuilder
from src.ai.vertex.coach import VertexCoach

from src.shared.logging import get_logger
from src.shared.trace import ensure_trace_id

logger = get_logger("query_pipeline")


class QueryPipeline:
    """
    AI READ PIPELINE (NOT DSL EXECUTION)

    FLOW:
    USER TEXT → QUERY → GRAPH → CONTEXT → AI → RESPONSE
    """

    def __init__(self):

        self.parser = QueryParser()
        self.graph = QueryEngine()
        self.context_builder = ContextBuilder()
        self.coach = VertexCoach()

    def handle(self, text: str, user_id: str, session_id: str):

        trace_id = ensure_trace_id()

        logger.info("QUERY_PIPELINE_START")

        # =========================
        # 1. SEMANTIC PARSE
        # =========================
        query = self.parser.parse(
            text=text,
            user_id=user_id,
            session_id=session_id,
            trace_id=trace_id
        )

        logger.info(f"QUERY_PARSED: {query.intent}")

        # =========================
        # 2. GRAPH RETRIEVAL
        # =========================
        graph_result = self.graph.fetch(query)

        logger.info(f"GRAPH_FETCHED: {graph_result.found}")

        # =========================
        # 3. CONTEXT BUILD
        # =========================
        context = self.context_builder.build(
            query=query,
            graph_result=graph_result
        )

        # =========================
        # 4. AI COACH RESPONSE
        # =========================
        response = self.coach.generate(context)

        logger.info("QUERY_PIPELINE_END")

        return {
            "trace_id": trace_id,
            "response": response
        }