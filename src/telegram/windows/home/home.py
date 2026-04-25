# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# DESCRIPTION:
# HOME UI window (getter only, no logic)
# =========================================

from src.services.user.user_profile import user_profile


async def get_home_data(dialog_manager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    profile = user_profile.get(user_id)

    name = (
        dialog_manager.event.from_user.username
        or dialog_manager.event.from_user.first_name
        or "User"
    )

    game_nick = profile.nickname if profile and profile.nickname else "—"

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Name: {name}\n"
            f"🎮 Game nick: {game_nick}\n"
            f"🎭 Role: {profile.role if profile else 'R3'}"
        )
    }