from backend_models.player_model import PlayerModel

class GameOverDetails:
    def __init__(self, winner: PlayerModel , loser: PlayerModel):
        self.winner_name = winner.name
        self.loser_name = loser.name
        self.winner_pin = winner.pin
        self.loser_pin = loser.pin
        self.winner_guess_count = winner.guess_count
