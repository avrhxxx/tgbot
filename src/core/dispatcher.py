from src.core.actions import Action

async def dispatch(action: Action, state):
    if action == Action.GO_HOME:
        state.screen = "home_r3"
        return state