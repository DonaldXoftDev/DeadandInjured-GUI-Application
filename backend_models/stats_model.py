from backend_models.player_model import PlayerModel

class StatDetails:
    def __init__(self, turn: PlayerModel):
        self.player_name:str = turn.name
        self.player_pin: list[int] = turn.pin
        self.player_guess: list[int] = turn.guess
        self.all_player_stats: list[StatDetails]
        self.player_guess_count: int = turn.guess_count
        self.feedback_history: list[str] = turn.feedback_history