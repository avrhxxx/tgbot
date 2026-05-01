# scripts/list_models.py

import asyncio
import aiohttp
import os


async def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Missing GEMINI_API_KEY")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

            print("\n=== AVAILABLE MODELS ===\n")
            print(data)


if __name__ == "__main__":
    asyncio.run(main())