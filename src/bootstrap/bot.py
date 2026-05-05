# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Minimal runtime entrypoint for Shadow AI System (BOOT CONTRACT)

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    """
    Minimal system bootstrap.
    Ensures Railway has a valid runtime entrypoint.
    """
    logger.info("🧠 Shadow AI System starting...")

    # TEMP: placeholder for CORE system init
    logger.info("CORE not yet attached - bootstrap OK")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())