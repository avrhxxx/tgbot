# src/google/firestore/client.py
# GROUP: google.firestore
# DESCRIPTION: Firestore GCP client wrapper (async-safe, minimal, production-ready)

import logging
from google.cloud import firestore
from concurrent.futures import ThreadPoolExecutor
from src.google.auth import load_google_credentials

logger = logging.getLogger("google.firestore")

_executor = ThreadPoolExecutor(max_workers=5)


class FirestoreClient:
    def __init__(self):
        # ✅ FIX: unified auth layer (ADC + Service Account fallback)
        credentials = load_google_credentials()

        self.db = firestore.Client(credentials=credentials)

        logger.info("🔥 Firestore client initialized (auth v2 mode)")

    # =========================
    # INTERNAL ASYNC WRAPPER
    # =========================
    async def _run(self, func, *args, **kwargs):
        loop = __import__("asyncio").get_event_loop()
        return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

    # =========================
    # INDEX LAYER (EXISTENCE SYSTEM)
    # =========================
    async def get_definition(self, object_type: str, name: str):
        doc_id = f"{object_type}/{name.lower().replace(' ', '_')}"
        ref = self.db.document(doc_id)

        doc = await self._run(ref.get)

        if not doc.exists:
            return None

        return doc.to_dict()

    async def set_definition(self, object_type: str, name: str, data: dict):
        doc_id = f"{object_type}/{name.lower().replace(' ', '_')}"
        ref = self.db.document(doc_id)

        payload = {
            **data,
            "name": name,
            "type": object_type,
        }

        await self._run(ref.set, payload, merge=True)

        logger.info("🔥 INDEX saved | %s", doc_id)
        return True

    # =========================
    # 🧠 KNOWLEDGE LAYER (NEW)
    # =========================
    async def set_knowledge(self, object_type: str, name: str, data: dict):
        """
        Separate namespace for semantic knowledge (NOT game index)
        """

        doc_id = f"knowledge/{object_type}/{name.lower().replace(' ', '_')}"
        ref = self.db.document(doc_id)

        payload = {
            **data,
            "name": name,
            "type": object_type,
        }

        await self._run(ref.set, payload, merge=True)

        logger.info("🧠 KNOWLEDGE saved | %s", doc_id)
        return True

    # =========================
    # EXISTS CHECK
    # =========================
    async def exists(self, object_type: str, name: str) -> bool:
        return await self.get_definition(object_type, name) is not None