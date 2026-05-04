# src/google/auth.py
# GROUP: google
# DESCRIPTION: Safe Google auth layer (ADC-first, Service Account fallback)

import json
import logging
import os
from typing import Any

from google.auth import default
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",  # ✅ FIX: required for Drive + Docs folder operations
]


def load_google_credentials() -> Any:
    """
    Google authentication layer.

    Priority:
    1. ADC (Vertex / GCP / Railway recommended)
    2. Service Account JSON fallback (env-based)
    """

    logger.info("🔐 Google auth init started")

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # =========================
    # 1. ADC MODE (BEST PRACTICE)
    # =========================
    if not raw:
        logger.info("🔵 ADC mode detected (no GOOGLE_SERVICE_ACCOUNT provided)")
        logger.info("🔵 Using Application Default Credentials...")

        creds, _ = default(scopes=SCOPES)

        logger.info("✅ ADC authentication successful")
        return creds

    # =========================
    # 2. SERVICE ACCOUNT FALLBACK
    # =========================
    logger.info("🟡 Service Account mode detected (env GOOGLE_SERVICE_ACCOUNT exists)")

    try:
        data = json.loads(raw)
        logger.info("🟢 Service account JSON parsed successfully")

    except Exception as err:
        logger.error("❌ Failed to parse GOOGLE_SERVICE_ACCOUNT JSON")
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from err

    required_fields = ["client_email", "private_key", "project_id"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        logger.error("❌ Missing fields in service account: %s", missing)
        raise ValueError(f"Missing fields in service account: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    logger.info("🔧 Service account normalized (private_key fixed)")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    logger.info("✅ Service Account authentication successful")
    logger.info("📧 Authenticated as: %s", data.get("client_email"))

    return credentials