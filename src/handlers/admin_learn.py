# src/handlers/admin_learn.py
# GROUP: handlers
# DESCRIPTION: Admin command to teach bot knowledge (/learn) - upgraded ingestion pipeline

import logging
import re
import aiohttp
from aiogram import Router
from aiogram.types import Message

from src.wiki.knowledge.firestore_client import FirestoreClient
from src.wiki.embeddings.client import EmbeddingClient

logger = logging.getLogger("handlers.admin.learn")

router = Router()

firestore = FirestoreClient()
embedding_client = EmbeddingClient()


# =========================
# OPTIONAL EXTRACTOR
# =========================
try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except Exception:
    TRAFILATURA_AVAILABLE = False


# =========================
# CLEANER FALLBACK
# =========================
def _clean_text(html: str) -> str:
    text = re.sub(r"<script.*?>.*?</script>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<.*?>", " ", text)
    return " ".join(text.split())


# =========================
# CHUNKER
# =========================
def _chunk_text(text: str, size: int = 800) -> list[str]:
    words = text.split()
    chunks = []

    current = []
    length = 0

    for w in words:
        current.append(w)
        length += 1

        if length >= size:
            chunks.append(" ".join(current))
            current = []
            length = 0

    if current:
        chunks.append(" ".join(current))

    return chunks


# =========================
# FETCH PAGE
# =========================
async def _fetch_page(url: str) -> str:
    try:
        headers = {"User-Agent": "shadow-bot/1.0"}
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return ""

                html = await resp.text()

                if TRAFILATURA_AVAILABLE:
                    try:
                        extracted = trafilatura.extract(html)
                        if extracted and len(extracted) > 200:
                            return extracted
                    except Exception as e:
                        logger.warning("Trafilatura failed: %s", e)

                return _clean_text(html)

    except Exception as e:
        logger.exception("Fetch failed: %s", e)
        return ""


# =========================
# /learn COMMAND
# =========================
@router.message(lambda m: m.text and m.text.startswith("/learn"))
async def learn_handler(message: Message):

    text = message.text or ""
    parts = text.split()

    if len(parts) < 3:
        await message.answer("Usage: /learn <topic> <url>")
        return

    topic = parts[1].strip().lower()
    url = parts[2].strip()

    await message.answer("📥 Processing knowledge...")

    content = await _fetch_page(url)

    if not content or len(content) < 200:
        await message.answer("❌ Failed to extract content.")
        return

    chunks = _chunk_text(content)

    try:
        saved = 0

        for chunk in chunks:
            embedding = embedding_client.embed(chunk)

            await firestore.add_knowledge(
                topic=topic,
                url=url,
                content=chunk,
                embedding=embedding,  # OK tylko jeśli FirestoreClient obsługuje
            )

            saved += 1

        await message.answer(f"✅ Learned {saved} knowledge chunks.")

    except Exception as e:
        logger.exception("Learning pipeline failed: %s", e)
        await message.answer("❌ Failed to save knowledge.")