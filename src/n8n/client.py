# =========================================
# FILE: src/n8n/client.py
# =========================================

import logging
import httpx
import asyncio
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class N8NClient:
    def __init__(self, base_url: str, timeout: float = 5.0, retries: int = 2):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    async def close(self):
        await self._client.aclose()

    async def call(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        last_error = None

        for attempt in range(self.retries + 1):
            try:
                response = await self._client.post(url, json=payload)
                response.raise_for_status()

                data: Dict[str, Any] = response.json()

                # FIX mypy: no Any return
                return dict(data)

            except Exception as e:
                last_error = e
                logger.warning(f"[N8N] attempt {attempt} failed: {e}")
                await asyncio.sleep(0.3 * (attempt + 1))

        logger.error(f"[N8N] FAILED: {last_error}")
        return None