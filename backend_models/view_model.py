from backend_models.game_screen_model import GameScreen
from backend_models.gameover_data_model import GameOverDetails
from backend_models.stats_model import StatDetails


class AppViewModel:
    def __init__(self,
                 screen: GameScreen,
                 data: any = None
                 ):
        self.screen = screen
        self.details = data


