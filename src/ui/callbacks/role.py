from aiogram.filters.callback_data import CallbackData


class RoleCB(CallbackData, prefix="role"):
    action: str   # np. "switch"
    role: str     # np. "R3", "R4", "R5"