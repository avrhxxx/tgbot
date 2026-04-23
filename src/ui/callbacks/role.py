from aiogram.filters.callback_data import CallbackData


class RoleCB(CallbackData, prefix="role"):
    """
    Role system callbacks.

    Replaces:
    - SWITCH_ROLE
    and future role actions.
    """

    action: str  # switch, set
    value: str | None = None