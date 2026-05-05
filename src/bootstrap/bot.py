# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Minimal runtime entrypoint + CORE pipeline smoke test (Shadow AI System)

import asyncio
import logging

from src.core.runtime.pipeline import Pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    logger.info("🧠 Shadow AI System BOOTING...")

    # =========================
    # CORE INITIALIZATION
    # =========================
    pipeline = Pipeline()

    logger.info("CORE pipeline initialized")

    # =========================
    # SMOKE TEST (CRITICAL)
    # =========================
    try:
        logger.info("Running CORE smoke test...")

        test_input = 'create hero "TestHero"'
        result = pipeline.handle(test_input)

        logger.info(f"CORE test result: {result}")

    except Exception as e:
        logger.exception("CORE smoke test failed: %s", e)

    logger.info("🚀 System is running (idle mode)")

    # =========================
    # KEEP PROCESS ALIVE
    # =========================
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())