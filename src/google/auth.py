# src/google/auth.py
# GROUP: google
# DESCRIPTION: Vertex-compatible auth (ADC-first, SA fallback)

import json
import logging
import os

from google.oauth2 import service_account
from google.auth import default

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]


def load_service_account():
    """
    Vertex-safe authentication loader.

    Priority:
    1. ADC (best for Vertex)
    2. Service Account JSON (fallback)
    """

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # =========================
    # 1. ADC MODE (VERTEX BEST PRACTICE)
    # =========================
    if not raw:
        logger.info("Using ADC authentication (recommended for Vertex)")
        creds, _ = default(scopes=SCOPES)
        return creds

    # =========================
    # 2. SERVICE ACCOUNT FALLBACK
    # =========================
    try:
        data = json.loads(raw)

    except Exception as e:
        raise RuntimeError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from e

    required_fields = ["client_email", "private_key", "project_id"]

    missing = [f for f in required_fields if f not in data]

    if missing:
        raise RuntimeError(f"Missing fields in service account: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    logger.info("Using Service Account auth: %s", data["client_email"])

    return credentials