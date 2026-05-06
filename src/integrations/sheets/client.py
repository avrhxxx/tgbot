# GROUP: integrations.sheets
# DESCRIPTION: Google Sheets registry layer (types/fields/relations admin view)

from typing import List, Dict, Any
import logging

logger = logging.getLogger("sheets")


class SheetsClient:
    """
    Sheets = HUMAN CONTROL PANEL
    Used for registries, NOT runtime graph.
    """

    def __init__(self):
        self.enabled = False  # enable when Google API ready

    # =========================================
    # TYPE REGISTRY SYNC
    # =========================================

    def sync_types(self, types: List[Dict[str, Any]]):
        if not self.enabled:
            logger.info("[Sheets disabled] sync_types")
            return

        logger.info(f"[Sheets] syncing types count={len(types)}")

    # =========================================
    # FIELD REGISTRY SYNC
    # =========================================

    def sync_fields(self, fields: List[Dict[str, Any]]):
        if not self.enabled:
            logger.info("[Sheets disabled] sync_fields")
            return

        logger.info(f"[Sheets] syncing fields count={len(fields)}")

    # =========================================
    # RELATION REGISTRY SYNC
    # =========================================

    def sync_relations(self, relations: List[Dict[str, Any]]):
        if not self.enabled:
            logger.info("[Sheets disabled] sync_relations")
            return

        logger.info(f"[Sheets] syncing relations count={len(relations)}")