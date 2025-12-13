from typing import Protocol
from backend_models.player_model import PlayerModel

class RequiredDetails(PlayerModel):
    def __init__(self, name, state, turn):
        super().__init__(name)
        self.state = state
        self.turn = turn


class ViewProtocol(Protocol):
    def __init__(self):
        ...

    def render_new_screen(self):
        ...

    def display_error_notification(self):
        ...

class GamePresenter:
    def __init__(self, view: ViewProtocol):
        self.view = view
