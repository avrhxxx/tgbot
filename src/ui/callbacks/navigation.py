from aiogram.filters.callback_data import CallbackData


class NavigationCB(CallbackData, prefix="nav"):
    """
    UI navigation layer:
    replaces ActionID navigation constants.
    """

    target: str  # home, events, settings, back