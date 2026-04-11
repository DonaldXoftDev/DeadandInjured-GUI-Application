from backend_models.player_model import PlayerModel
from backend_models.game_screen_model import GameScreen

class MainGameModel:
    def __init__(self):
        self.players: list[PlayerModel] = []
        self.current_screen: GameScreen = GameScreen.MODE_SELECT
        self.current_index: int = -1
        self.screen_turn: int = 0
        self.current_player: PlayerModel | None = None


    def reset_data(self):
        self.players: list[PlayerModel] = []
        self.current_screen: GameScreen = GameScreen.MODE_SELECT
        self.current_index: int = -1
        self.screen_turn = 0
        self.current_player: PlayerModel | None = None

