from aiogram.filters.callback_data import CallbackData


class EventCB(CallbackData, prefix="event"):
    """
    Event interaction system.

    Replaces:
    - JOIN_EVENT
    - LEAVE_EVENT
    - OPEN_EVENT
    """

    action: str   # join, leave, open, view
    event_id: str | None = None