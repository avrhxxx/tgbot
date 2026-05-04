# src/google/auth.py
# GROUP: google
# DESCRIPTION: Production-safe dual auth system (Vertex ADC + Google Service Account split, strict singleton)

import json
import logging
import os
from typing import Any, Optional, Tuple

from google.auth import default
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

# =========================
# SCOPES (Google APIs ONLY)
# =========================
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# =========================
# SINGLETON CACHE
# =========================
_ADC_CREDS: Optional[Any] = None
_SA_CREDS: Optional[Any] = None


# =========================================================
# VERTEX AI (ADC ONLY - NO JSON, NO CONFIG, NO EXCEPTIONS)
# =========================================================
def get_vertex_credentials() -> Any:
    global _ADC_CREDS

    if _ADC_CREDS:
        return _ADC_CREDS

    logger.info("🤖 Loading Vertex AI ADC credentials...")

    creds, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    _ADC_CREDS = creds

    logger.info("✅ Vertex AI ADC initialized")
    logger.info("TYPE: %s", type(creds).__name__)

    return creds


# =========================================================
# GOOGLE APIs (SERVICE ACCOUNT ONLY)
# =========================================================
def load_google_credentials() -> Any:
    global _SA_CREDS

    if _SA_CREDS:
        return _SA_CREDS

    logger.info("📁 Loading Google Service Account credentials...")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT env is missing")

    try:
        data = json.loads(raw)
    except Exception as e:
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from e

    required = ["client_email", "private_key", "project_id"]
    missing = [x for x in required if x not in data]

    if missing:
        raise ValueError(f"Missing service account fields: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    creds = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    _SA_CREDS = creds

    logger.info("✅ Google Service Account initialized")
    logger.info("EMAIL: %s", creds.service_account_email)

    return creds