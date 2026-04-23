from aiogram.filters.callback_data import CallbackData


class AppCB(CallbackData, prefix="app"):
    """
    Unified callback wrapper.

    Replaces ActionID + UI_TO_ACTION_MAP concept.

    Acts as a SINGLE entry point for all UI actions.
    """

    scope: str   # nav | event | role
    action: str
    payload: str | None = None