# src/google/auth.py
# GROUP: google
# DESCRIPTION: Service Account loader (Node-style safe parsing equivalent)

import json
import logging
from google.oauth2 import service_account

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform"
]


def load_service_account():
    """
    Loads and validates service account from env (Node-style equivalent).
    """

    import os

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

    # normalize private key (Node-style fix)
    data["private_key"] = data["private_key"].replace("\\n", "\n")

    credentials = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    logger.info("Google SA loaded for: %s", data["client_email"])

    return credentials