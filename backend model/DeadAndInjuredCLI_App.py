from player_model import PlayerModel
from computer_player import  ComputerPlayer
from feedback_mechanism import Feedback
from logic import Logic
import json

class DeadAndInjuredCLIApp:
    def __init__(self, player: PlayerModel, opponent: PlayerModel | ComputerPlayer):
        self.player = player
        self.opponent = opponent
        self.LEADERBOARD_FILE = 'leaderboard.json'


    def initialize_player_pins(self,logic):
        player_pin = logic.get_player_pin(self.player.name.title())
        if not player_pin:
            print('Invalid pin entered')
            return False

        self.player.pin = player_pin
        print(f'{self.player.name.title()} has chosen a valid pin...\n')

        if not self.opponent.is_human:
            self.opponent.computer_pin()
            print(f'{self.opponent.name.title()} has generated a valid pin...')
            return True

        else:
            opponent_pin = logic.get_player_pin(self.opponent.name.title())
            if not opponent_pin:
                print('Invalid pin entered\n')
                return False

            self.opponent.pin = opponent_pin
            print(f'{self.opponent.name.title()} has chosen a valid pin...')
            return True


    def run_cli_game(self):
        logic = Logic()

        entering_pin = True
        while entering_pin:
           if not self.initialize_player_pins(logic):
               continue
           break


        # is_guessing = True
        # while is_guessing:
        #     player_guess = logic.get_player_guess()
        #     if not player_guess:
        #         print('Invalid guess entered')
        #         is_guessing = True
        #
        #     self.player.guess = player_guess
        #     print(f'{self.player.name.title()} has guessed picked a guess...')
        #
        #     player_feedback_data = logic.compare_pin_to_guess(self.player, self.opponent)
        #     if not player_feedback_data:
        #         print(f'A problem occurred while {self.player.name.title()} guess to {self.opponent.name.title()} pin')
        #         is_guessing = True
        #
        #     player_feedback_message = Feedback(player_feedback_data).feedback_result()
        #     print(f'Feedback to {self.player.name.title()} after comparison is {player_feedback_message}')
        #
        #     logic.update_feedback_history(self.player, feedback=player_feedback_message)
        #
        #     if logic.has_won(self.player):
        #         logic.save_winner(self.LEADERBOARD_FILE, self.player)
        #         break


def create_player() -> PlayerModel | ComputerPlayer:
    entering_name = True
    new_player = None
    while entering_name:
        name = input('Enter your player name: ')
        if not name:
            print('Please enter a player name.')
            continue
        entering_name = False

        new_player = PlayerModel(name)
        print(f'Player {new_player.name.title()} created...\n')
    return new_player

if __name__ == '__main__':
   player_1 = create_player()
   player_2 = create_player()

   game_cli_app = DeadAndInjuredCLIApp(player_1, player_2)
   game_cli_app.run_cli_game()











