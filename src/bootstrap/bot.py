# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: CORE-only runtime entrypoint (no external dependencies)

import asyncio
from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("bootstrap")


async def main():
    logger.info("🧠 CORE SYSTEM START")

    pipeline = Pipeline()

    test_input = 'create hero "TestHero"'
    result = pipeline.handle(test_input)

    logger.info(f"CORE RESULT: {result}")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())