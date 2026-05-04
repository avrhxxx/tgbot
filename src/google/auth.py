# src/google/auth.py
# GROUP: google
# DESCRIPTION: Safe Google auth layer (ADC-first, Service Account fallback + TRUE singleton + full identity debug tracing)

import json
import logging
import os
from typing import Any

from google.auth import default
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

# =========================
# FULL SCOPES (CRITICAL)
# =========================
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# =========================
# 🔥 SINGLETON CACHE (FIX)
# =========================
_CACHED_CREDENTIALS: Any = None


# =========================
# DEBUG CORE
# =========================
def _debug_credentials(creds: Any, label: str = "CREDS") -> None:
    logger.info("🧪 ===== GOOGLE AUTH DEBUG [%s] =====", label)
    logger.info("TYPE: %s", type(creds))

    logger.info("SERVICE ACCOUNT EMAIL: %s", getattr(creds, "service_account_email", None))
    logger.info("CLIENT EMAIL: %s", getattr(creds, "client_email", None))
    logger.info("PROJECT ID: %s", getattr(creds, "project_id", None))

    logger.info("HAS TOKEN: %s", hasattr(creds, "token"))
    logger.info("HAS WITH_SCOPES: %s", hasattr(creds, "with_scopes"))

    logger.info("SCOPES: %s", getattr(creds, "scopes", None))
    logger.info("ADC DETECTED: %s", creds.__class__.__name__.lower().find("default") != -1)

    logger.info("======================================")


# =========================
# SCOPE NORMALIZATION
# =========================
def _normalize_scopes(creds: Any) -> Any:
    if hasattr(creds, "with_scopes"):
        try:
            return creds.with_scopes(SCOPES)
        except Exception as e:
            logger.warning("⚠️ Failed to normalize scopes: %s", e)
    return creds


# =========================
# SINGLE ENTRYPOINT (FIXED)
# =========================
def load_google_credentials() -> Any:
    """
    TRUE SINGLETON:
    - One identity per runtime
    - Prevents Drive/Docs mismatch auth bugs
    """

    global _CACHED_CREDENTIALS

    if _CACHED_CREDENTIALS is not None:
        logger.info("♻️ Returning cached Google credentials (SINGLETON HIT)")
        return _CACHED_CREDENTIALS

    logger.info("🔐 Google auth init started (FIRST INIT ONLY)")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # =========================
    # 1. ADC MODE
    # =========================
    if not raw:
        logger.info("🔵 ADC mode detected")

        creds, _ = default(scopes=SCOPES)
        creds = _normalize_scopes(creds)

        logger.info("✅ ADC authentication successful")
        _debug_credentials(creds, "ADC")

        _CACHED_CREDENTIALS = creds
        return creds

    # =========================
    # 2. SERVICE ACCOUNT MODE
    # =========================
    logger.info("🟡 Service Account mode detected")

    try:
        data = json.loads(raw)
    except Exception as err:
        logger.error("❌ Failed to parse GOOGLE_SERVICE_ACCOUNT JSON")
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from err

    required_fields = ["client_email", "private_key", "project_id"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        logger.error("❌ Missing fields in service account: %s", missing)
        raise ValueError(f"Missing fields in service account: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    creds = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    creds = _normalize_scopes(creds)

    logger.info("✅ Service Account authentication successful")
    _debug_credentials(creds, "SERVICE_ACCOUNT")

    _CACHED_CREDENTIALS = creds
    return creds