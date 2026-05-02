# src/handlers/admin_learn.py
# GROUP: handlers
# DESCRIPTION: Admin command to teach bot knowledge (/learn)

import logging
import re

import aiohttp
from aiogram import Router
from aiogram.types import Message

from src.wiki.knowledge.firestore_client import FirestoreClient

logger = logging.getLogger("handlers.admin.learn")

router = Router()

firestore = FirestoreClient()


# =========================
# SIMPLE HTML CLEANER
# =========================
def _clean_text(html: str) -> str:
    text = re.sub(r"<script.*?>.*?</script>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<.*?>", " ", text)
    text = " ".join(text.split())
    return text[:3000]


# =========================
# FETCH PAGE
# =========================
async def _fetch_page(url: str) -> str:
    try:
        headers = {
            "User-Agent": "shadow-bot/1.0"
        }

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return ""

                html = await resp.text()
                return _clean_text(html)

    except Exception as e:
        logger.exception("Fetch failed: %s", e)
        return ""


# =========================
# /learn COMMAND (ADMIN ONLY)
# =========================
@router.message(lambda m: m.text and m.text.startswith("/learn"))
async def learn_handler(message: Message):
    """
    Usage:
    /learn <topic> <url>
    """

    text = message.text or ""
    parts = text.split()

    if len(parts) < 3:
        await message.answer("Usage: /learn <topic> <url>")
        return

    topic = parts[1].strip().lower()
    url = parts[2].strip()

    await message.answer("📥 Learning from source...")

    content = await _fetch_page(url)

    if not content or len(content) < 200:
        await message.answer("❌ Failed to extract useful content.")
        return

    try:
        await firestore.add_knowledge(
            topic=topic,
            url=url,
            content=content[:3000]
        )

        await message.answer("✅ Knowledge saved.")

    except Exception as e:
        logger.exception("Firestore save failed: %s", e)
        await message.answer("❌ Failed to save knowledge.")