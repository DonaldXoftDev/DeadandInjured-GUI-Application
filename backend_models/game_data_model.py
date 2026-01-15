from backend_models.player_model import PlayerModel

class MainGameModel:
    def __init__(self):
        self.players: list[PlayerModel] = []
        self.current_screen: str = 'MODE_SELECT'
        self.current_index: int = 0
        self.screen_turn: int = 0
        self.current_player: PlayerModel | None = None

