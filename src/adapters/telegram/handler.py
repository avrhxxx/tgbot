from src.core.runtime.pipeline import Pipeline
from src.core.runtime.query_pipeline import QueryPipeline
from src.shared.logging import get_logger

import uuid

logger = get_logger("TelegramAdapter")


class TelegramHandler:

    def __init__(self):
        self.pipeline = Pipeline()
        self.query_pipeline = QueryPipeline()   # 🔥 DODANE

    async def handle_text(self, text: str) -> dict:

        trace_id = str(uuid.uuid4())

        logger.info(f"[trace={trace_id}] input: {text}")

        try:

            # =========================
            # DSL PATH (WRITE SYSTEM)
            # =========================
            if text.startswith("/dsl"):
                result = self.pipeline.handle(text.replace("/dsl", "").strip())

            # =========================
            # QUERY PATH (AI READ SYSTEM)
            # =========================
            else:
                result = self.query_pipeline.handle(
                    text=text,
                    user_id="telegram_user",
                    session_id="default"
                )

            response = {
                "status": "ok",
                "trace_id": trace_id,
                "result": result
            }

        except Exception as e:

            logger.error(f"[trace={trace_id}] error: {str(e)}")

            response = {
                "status": "error",
                "trace_id": trace_id,
                "error": str(e)
            }

        logger.info(f"[trace={trace_id}] output ready")

        return response


handler = TelegramHandler()


async def handle_telegram_text(text: str) -> dict:
    return await handler.handle_text(text)