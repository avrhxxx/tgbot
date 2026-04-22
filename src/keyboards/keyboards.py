from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import load_config
from src.core.state_store import state_store
from src.ui.definitions.action_ids import ActionID

config = load_config()


# =========================
# 🧭 GLOBAL BUTTONS
# =========================

def back_button():
    return InlineKeyboardButton(
        text="⬅️ Back",
        callback_data=ActionID.BACK
    )


def home_button():
    return InlineKeyboardButton(
        text="🏠 Home",
        callback_data=ActionID.GO_HOME
    )


# =========================
# 🎭 DEMO ROLE SWITCH
# =========================

def demo_role_switch_button(user_id: int):
    current = state_store.get_demo_role(user_id) or "R3"

    next_role_map = {
        "R3": "R4",
        "R4": "R5",
        "R5": "R3",
    }

    next_role = next_role_map.get(current, "R3")

    return InlineKeyboardButton(
        text=f"🎭 Switch Role ({current} → {next_role})",
        callback_data=f"demo:switch_role:{next_role}"
    )


# =========================
# 🧠 HOME KEYBOARD FACTORY
# =========================

def home_keyboard(role: str, user_id: int = None):
    if role == "R3":
        return _home_keyboard_r3(user_id)

    # R4 + R5 share same UI base
    return _home_keyboard_admin(user_id, role)


# =========================
# 🟢 R3 HOME (USER)
# =========================

def _home_keyboard_r3(user_id: int = None):
    keyboard = [
        [
            InlineKeyboardButton("📅 Events", callback_data=ActionID.GO_EVENTS),
            InlineKeyboardButton("⚡ Quick Join", callback_data=ActionID.JOIN_EVENT),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data=ActionID.GO_SETTINGS),
            InlineKeyboardButton("❓ Help", callback_data=ActionID.GO_HOME),
        ],
    ]

    if config.features.demo_mode and user_id:
        keyboard.insert(0, [demo_role_switch_button(user_id)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# =========================
# 🟡 ADMIN HOME (R4 + R5)
# =========================

def _home_keyboard_admin(user_id: int = None, role: str = "R4"):
    keyboard = [
        [
            InlineKeyboardButton("🧭 Event Management", callback_data=ActionID.GO_EVENT_MANAGEMENT),
        ],
        [
            InlineKeyboardButton("👥 User Management", callback_data=ActionID.GO_HOME),
        ],
        [
            InlineKeyboardButton("🧪 Pre-Register User", callback_data=ActionID.GO_HOME),
        ],
    ]

    # =========================
    # 🔴 R5 ONLY (permission overlay)
    # =========================
    if role == "R5":
        keyboard.append([
            InlineKeyboardButton("⚡ Emergency Override", callback_data=ActionID.GO_HOME),
        ])

    keyboard.append([
        InlineKeyboardButton("⚙️ Settings", callback_data=ActionID.GO_SETTINGS),
        InlineKeyboardButton("🏠 Home", callback_data=ActionID.GO_HOME),
    ])

    if config.features.demo_mode and user_id:
        keyboard.insert(0, [demo_role_switch_button(user_id)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# =========================
# 📡 EVENTS
# =========================

def events_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [back_button(), home_button()]
    ])


# =========================
# ⚙️ SETTINGS
# =========================

def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [back_button(), home_button()]
    ])