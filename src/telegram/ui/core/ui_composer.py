# =========================================
# GROUP: telegram.ui.core
# FILE: ui_composer.py
# DESCRIPTION:
# Composes UI based on user role using feature injection.
# No role logic inside windows.
# =========================================

import logging
from typing import List

from src.telegram.permissions.context import UserContext
from src.telegram.ui.core.feature_resolver import resolve_features

logger = logging.getLogger(__name__)


class UIComposer:
    """
    Builds final UI payload (text + buttons) based on role features.
    """

    def compose_home(self, user: UserContext, base_text: str, base_buttons: list):
        logger.info("Composing Home UI | user=%s role=%s", user.user_id, user.role)

        features = resolve_features("home", user.role)

        buttons = list(base_buttons)

        for feature in features:
            buttons.extend(feature.get("buttons", []))

        return {
            "text": base_text,
            "buttons": buttons,
        }


ui_composer = UIComposer()