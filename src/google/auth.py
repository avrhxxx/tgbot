# src/google/auth.py
# GROUP: google
# DESCRIPTION: Stable dual-auth system (Vertex ADC + Google SA isolated, no cross-cache)

import json
import logging
import os
from typing import Any, Optional, Tuple

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
# SEPARATE CACHES (🔥 FIX CORE)
# =========================
_ADC_CREDS: Optional[Any] = None
_SA_CREDS: Optional[Any] = None


def _debug(creds: Any, source: str) -> None:
    logger.info("🧪 ===== GOOGLE AUTH DEBUG (%s) =====", source)
    logger.info("TYPE: %s", type(creds).__name__)
    logger.info("EMAIL: %s", getattr(creds, "service_account_email", None) or getattr(creds, "client_email", None))
    logger.info("PROJECT: %s", getattr(creds, "project_id", None))
    logger.info("====================================")


# =========================
# VERTEX AI (ADC ONLY)
# =========================
def get_vertex_credentials() -> Any:
    global _ADC_CREDS

    if _ADC_CREDS:
        return _ADC_CREDS

    logger.info("🤖 Loading Vertex AI ADC credentials...")

    creds, _ = default(scopes=[
        "https://www.googleapis.com/auth/cloud-platform"
    ])

    _ADC_CREDS = creds

    logger.info("✅ Vertex AI ADC ready")
    _debug(creds, "VERTEX_ADC")

    return creds


# =========================
# GOOGLE APIs (SERVICE ACCOUNT ONLY)
# =========================
def load_google_credentials() -> Any:
    global _SA_CREDS

    if _SA_CREDS:
        return _SA_CREDS

    logger.info("📁 Loading Google API Service Account credentials...")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    if not raw:
        raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT")

    try:
        data = json.loads(raw)
    except Exception as err:
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from err

    required = ["client_email", "private_key", "project_id"]
    missing = [x for x in required if x not in data]

    if missing:
        raise ValueError(f"Missing SA fields: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    creds = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    _SA_CREDS = creds

    logger.info("✅ Google Service Account ready")
    _debug(creds, "SERVICE_ACCOUNT")

    return creds