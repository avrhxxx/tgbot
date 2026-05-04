# src/google/auth.py
# GROUP: google
# DESCRIPTION: Singleton-safe Google auth (ADC-first, config-aware, fully scoped, debug-ready)

import json
import logging
from typing import Any, Optional

from google.auth import default
from google.oauth2 import service_account

from src.config.config import load_config

logger = logging.getLogger("google.auth")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# =========================
# SINGLETON CACHE
# =========================
_CACHED_CREDS: Optional[Any] = None


def _debug(creds: Any, source: str) -> None:
    logger.info("🧪 ===== GOOGLE AUTH DEBUG (%s) =====", source)
    logger.info("TYPE: %s", type(creds).__name__)
    logger.info("EMAIL: %s", getattr(creds, "service_account_email", None) or getattr(creds, "client_email", None))
    logger.info("PROJECT: %s", getattr(creds, "project_id", None))
    logger.info("SCOPES: %s", getattr(creds, "scopes", None))
    logger.info("HAS TOKEN: %s", hasattr(creds, "token"))
    logger.info("====================================")


def _apply_scopes(creds: Any) -> Any:
    """
    Forces consistent scopes across ADC + SA.
    Prevents silent Docs 403 despite valid auth.
    """
    if hasattr(creds, "with_scopes"):
        try:
            return creds.with_scopes(SCOPES)
        except Exception as e:
            logger.warning("⚠️ Scope normalization failed: %s", e)
    return creds


def load_google_credentials() -> Any:
    global _CACHED_CREDS

    if _CACHED_CREDS is not None:
        logger.info("♻️ Reusing cached Google credentials")
        return _CACHED_CREDS

    logger.info("🔐 Initializing Google credentials (first run only)")

    # =========================
    # SINGLE SOURCE OF TRUTH
    # =========================
    cfg = load_config()
    raw = None

    if cfg.google.service_account:
        raw = json.dumps(cfg.google.service_account)

    # =========================
    # 1. ADC MODE
    # =========================
    if not raw:
        creds, _ = default(scopes=SCOPES)
        creds = _apply_scopes(creds)

        _CACHED_CREDS = creds

        logger.info("✅ ADC credentials loaded")
        _debug(creds, "ADC")

        return creds

    # =========================
    # 2. SERVICE ACCOUNT MODE
    # =========================
    try:
        data = json.loads(raw)
    except Exception as err:
        raise ValueError("Invalid service account JSON in config") from err

    required = ["client_email", "private_key", "project_id"]
    missing = [x for x in required if x not in data]

    if missing:
        raise ValueError(f"Missing service account fields: {missing}")

    data["private_key"] = data["private_key"].replace("\\n", "\n")

    creds = service_account.Credentials.from_service_account_info(
        data,
        scopes=SCOPES,
    )

    creds = _apply_scopes(creds)

    _CACHED_CREDS = creds

    logger.info("✅ Service Account credentials loaded")
    _debug(creds, "SERVICE_ACCOUNT")

    return creds