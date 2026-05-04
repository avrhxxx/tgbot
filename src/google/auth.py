# src/google/auth.py
# GROUP: google
# DESCRIPTION: Safe Google auth layer (ADC-first, Service Account fallback + full identity debug tracing)

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
# DEBUG CORE (IMPORTANT)
# =========================
def _debug_credentials(creds: Any, label: str = "CREDS") -> None:
    """
    Hard identity dump for debugging Google auth issues.
    """

    logger.info("🧪 ===== GOOGLE AUTH DEBUG [%s] =====", label)
    logger.info("TYPE: %s", type(creds))

    # identity signals
    logger.info("SERVICE ACCOUNT EMAIL: %s", getattr(creds, "service_account_email", None))
    logger.info("CLIENT EMAIL: %s", getattr(creds, "client_email", None))
    logger.info("PROJECT ID: %s", getattr(creds, "project_id", None))

    # capability signals
    logger.info("HAS TOKEN: %s", hasattr(creds, "token"))
    logger.info("HAS WITH_SCOPES: %s", hasattr(creds, "with_scopes"))

    # scopes (critical for Docs API)
    logger.info("SCOPES: %s", getattr(creds, "scopes", None))

    # ADC hint
    logger.info("ADC DETECTED: %s", creds.__class__.__name__.lower().find("default") != -1)

    logger.info("======================================")


def _normalize_scopes(creds: Any) -> Any:
    """
    Ensures consistent scopes across all credential types.
    """
    if hasattr(creds, "with_scopes"):
        try:
            return creds.with_scopes(SCOPES)
        except Exception as e:
            logger.warning("⚠️ Failed to normalize scopes: %s", e)
    return creds


# =========================
# MAIN AUTH ENTRYPOINT
# =========================
def load_google_credentials() -> Any:
    """
    Google authentication layer.

    Priority:
    1. ADC (Vertex / GCP / Railway recommended)
    2. Service Account JSON fallback
    """

    logger.info("🔐 Google auth init started")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # =========================
    # 1. ADC MODE
    # =========================
    if not raw:
        logger.info("🔵 ADC mode detected (no SERVICE ACCOUNT JSON)")

        creds, _ = default(scopes=SCOPES)
        creds = _normalize_scopes(creds)

        logger.info("✅ ADC authentication successful")

        _debug_credentials(creds, "ADC")

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

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    credentials = _normalize_scopes(credentials)

    logger.info("✅ Service Account authentication successful")

    _debug_credentials(credentials, "SERVICE_ACCOUNT")

    return credentials