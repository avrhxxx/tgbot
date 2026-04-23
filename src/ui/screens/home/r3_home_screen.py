# src/ui/screens/home/r3_home_screen.py

from ui.screen_contracts import ScreenResult, ScreenContext
from ui.keyboards.home.r3_home_kb import build_r3_home_kb


async def render(context: ScreenContext) -> ScreenResult:
    app = context["app"]
    user_id = context["user_id"]

    # -------------------------
    # USER DATA FETCH (via app layer)
    # -------------------------
    user = await app.services.user_service.get_user(user_id)

    telegram_first_name = getattr(user, "first_name", None)
    telegram_username = getattr(user, "telegram_username", None)
    game_nick = getattr(user, "game_nick", None)

    # -------------------------
    # WELCOME RESOLUTION
    # -------------------------
    if telegram_first_name:
        welcome_name = telegram_first_name
    elif telegram_username:
        welcome_name = telegram_username
    else:
        welcome_name = "Telegram User"

    # -------------------------
    # SAFE FALLBACKS
    # -------------------------
    if not game_nick:
        game_nick = "Not set"

    # Role is static for this screen (R3)
    role = "R3"

    # -------------------------
    # UTC DATE (UI ONLY)
    # -------------------------
    today_utc = app.time_service.utcnow().strftime("%Y-%m-%d")

    # -------------------------
    # TEXT RENDER
    # -------------------------
    text = (
        "🏠 Home Panel\n\n"
        f"Welcome, {welcome_name}\n\n"
        f"Game Nick: {game_nick}\n\n"
        f"Role: {role}\n\n"
        f"Today is: {today_utc} (UTC)"
    )

    return {
        "text": text,
        "keyboard": build_r3_home_kb()
    }