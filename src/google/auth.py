# src/google/auth.py
# GROUP: google
# DESCRIPTION: Safe Google auth layer (ADC-first, Service Account fallback + strong debug visibility)

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
    # 1. ADC MODE
    # =========================
    if not raw:
        logger.info("🔵 ADC mode detected")
        logger.info("🔵 Using Application Default Credentials...")

        creds, _ = default(scopes=SCOPES)

        # =========================
        # DEBUG FINGERPRINT (IMPORTANT)
        # =========================
        logger.info("✅ ADC authentication successful")
        logger.info("🔑 AUTH TYPE: %s", type(creds).__name__)
        logger.info("📧 AUTH EMAIL: %s", getattr(creds, "service_account_email", None))
        logger.info("📦 SCOPES COUNT: %s", len(SCOPES))

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

    # fix private key format
    data["private_key"] = data["private_key"].replace("\\n", "\n")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    # =========================
    # DEBUG FINGERPRINT (IMPORTANT)
    # =========================
    logger.info("✅ Service Account authentication successful")
    logger.info("🔑 AUTH TYPE: %s", type(credentials).__name__)
    logger.info("📧 AUTH EMAIL: %s", data.get("client_email"))
    logger.info("📦 SCOPES COUNT: %s", len(SCOPES))

    return credentials