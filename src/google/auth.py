# src/google/auth.py
# GROUP: google
# DESCRIPTION: Singleton-safe Google auth (ADC-first, stable scoped identity)

import json
import logging
import os
from typing import Any, Optional

from google.auth import default
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# =========================
# SINGLETON CACHE (🔥 FIX)
# =========================
_CACHED_CREDS: Optional[Any] = None


def _debug(creds: Any) -> None:
    logger.info("🧪 AUTH DEBUG")
    logger.info("TYPE: %s", type(creds))
    logger.info("EMAIL: %s", getattr(creds, "service_account_email", None) or getattr(creds, "client_email", None))
    logger.info("SCOPES: %s", getattr(creds, "scopes", None))


def load_google_credentials() -> Any:
    global _CACHED_CREDS

    if _CACHED_CREDS:
        logger.info("♻️ Reusing cached Google credentials")
        return _CACHED_CREDS

    logger.info("🔐 Building Google credentials (FIRST INIT ONLY)")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # =========================
    # ADC
    # =========================
    if not raw:
        creds, _ = default(scopes=SCOPES)
        _CACHED_CREDS = creds

        logger.info("✅ ADC credentials loaded")
        _debug(creds)

        return creds

    # =========================
    # SERVICE ACCOUNT
    # =========================
    data = json.loads(raw)
    data["private_key"] = data["private_key"].replace("\\n", "\n")

    creds = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    _CACHED_CREDS = creds

    logger.info("✅ Service account credentials loaded")
    _debug(creds)

    return creds