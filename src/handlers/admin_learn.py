# src/handlers/admin_learn.py
# GROUP: handlers
# DESCRIPTION: Admin command to teach bot knowledge (/learn)

import logging
import re

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
    text = re.sub(r"<style.*?>.*?</style>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<.*?>", " ", text)
    text = " ".join(text.split())
    return text[:3000]


# =========================
# FETCH PAGE
# =========================
async def _fetch_page(url: str) -> str:
    import aiohttp

    try:
        headers = {
            "User-Agent": "shadow-bot/1.0"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return ""

                html = await resp.text()
                return _clean_text(html)

    except Exception as e:
        logger.exception("Fetch failed: %s", e)
        return ""


# =========================
# /learn COMMAND
# =========================
@router.message()
async def learn_handler(message: Message):
    """
    Usage:
    /learn heroes https://site.com/page
    """

    text = message.text or ""

    if not text.startswith("/learn"):
        return

    parts = text.split()

    if len(parts) < 3:
        await message.answer("Usage: /learn <topic> <url>")
        return

    _, topic, url = parts[0], parts[1], parts[2]

    await message.answer("📥 Learning from source...")

    content = await _fetch_page(url)

    if not content or len(content) < 200:
        await message.answer("❌ Failed to extract useful content.")
        return

    await firestore.add_knowledge(topic, url, content)

    await message.answer("✅ Knowledge saved.")