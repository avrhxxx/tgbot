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

# =========================
# FULL SCOPES (CRITICAL FIX)
# =========================
SCOPES = [
    # Core GCP
    "https://www.googleapis.com/auth/cloud-platform",

    # Sheets
    "https://www.googleapis.com/auth/spreadsheets",

    # Drive (files + folders)
    "https://www.googleapis.com/auth/drive",

    # Docs API (THIS WAS MISSING / INCONSISTENT IN PRACTICE)
    "https://www.googleapis.com/auth/documents",
]


def _normalize_scopes(creds: Any) -> Any:
    """
    Ensures credentials are consistently scoped across services.
    Prevents partial auth edge cases (Drive OK, Docs FAIL).
    """
    if hasattr(creds, "with_scopes"):
        try:
            return creds.with_scopes(SCOPES)
        except Exception:
            return creds
    return creds


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

        creds = _normalize_scopes(creds)

        logger.info("✅ ADC authentication successful")
        logger.info("📦 scopes=%s", len(SCOPES))

        return creds

    # =========================
    # 2. SERVICE ACCOUNT MODE
    # =========================
    logger.info("🟡 Service Account mode detected")

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

    # fix newline encoding
    data["private_key"] = data["private_key"].replace("\\n", "\n")

    logger.info("🔧 Service account normalized")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    credentials = _normalize_scopes(credentials)

    logger.info("✅ Service Account authentication successful")
    logger.info("📧 Authenticated as: %s", data.get("client_email"))
    logger.info("📦 scopes=%s", len(SCOPES))

    return credentials