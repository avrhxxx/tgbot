# src/google/auth.py
# GROUP: google
# DESCRIPTION: Central Google Service Account auth (Vertex + Firebase + Sheets ready)

import json
import logging
import os
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/datastore",
    "https://www.googleapis.com/auth/spreadsheets",
]


def load_service_account():
    """
    Central Google auth (used by Vertex, Firestore, Sheets).
    """

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT not provided")

    try:
        data = json.loads(raw)

    except Exception as e:
        raise RuntimeError("Invalid GOOGLE_SERVICE_ACCOUNT JSON") from e

    required_fields = ["client_email", "private_key", "project_id"]

    missing = [f for f in required_fields if f not in data]

    if missing:
        raise RuntimeError(f"Missing fields in service account: {missing}")

    # normalize key
    data["private_key"] = data["private_key"].replace("\\n", "\n")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    logger.info("Google SA loaded: %s", data["client_email"])

    return credentials