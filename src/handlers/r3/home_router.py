# src/handlers/r3/home_router.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


# =========================
# EVENTS
# =========================
@router.callback_query(F.data == "nav.events")
async def events(callback: CallbackQuery, **data):
    await callback.message.answer(
        "📅 Events module is coming soon.\n\n"
        "Next stage: Event Browser (OPEN + RESERVOIR)"
    )
    await callback.answer()


# =========================
# QUICK JOIN
# =========================
@router.callback_query(F.data == "nav.quick_join")
async def quick_join(callback: CallbackQuery, **data):
    await callback.message.answer(
        "⚡ Quick Join\n\n"
        "Checking available events..."
    )

    # placeholder logic (future engine hook)
    await callback.message.answer(
        "No active events found (MVP placeholder)."
    )

    await callback.answer()


# =========================
# SETTINGS
# =========================
@router.callback_query(F.data == "nav.settings")
async def settings(callback: CallbackQuery, **data):
    await callback.message.answer(
        "⚙️ Settings\n\n"
        "Game Nick editing coming next stage."
    )
    await callback.answer()


# =========================
# HELP
# =========================
@router.callback_query(F.data == "nav.help")
async def help_menu(callback: CallbackQuery, **data):
    await callback.message.answer(
        "❓ Help\n\n"
        "• Events → browse and join events\n"
        "• Quick Join → auto-join best event\n"
        "• Settings → manage your profile\n"
    )
    await callback.answer()