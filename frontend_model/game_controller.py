from backend_models.player_model import PlayerModel


class GameController:
    def __init__(self, model):
        self.model = model


    def get_current_player(self):
        return self.model.all_players[self.model.current_player_index]


    def total_players(self):
        return len(self.model.all_players)

    def get_next_player(self):
        total_players = self.total_players()
        next_index = (self.model.current_player_index + 1) % total_players
        self.model.current_player_index = next_index
        return self.model.all_players[next_index]

    def create_players(self,mode):
        if mode == 'H_Vs_C':
            comp_player = PlayerModel()
            comp_player.is_human = False
            comp_player.name = 'Computer'

            #human_player
            human_player = PlayerModel()

            self.model.all_players.extend([comp_player, human_player])

        else:
            self.model.all_players.extend([PlayerModel() for _ in range(2)])

    def save_player_detail(self,name,pin):
        current_player = self.get_current_player()
        current_player.name = name
        current_player.pin = pin















