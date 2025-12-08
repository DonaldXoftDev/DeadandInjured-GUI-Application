from player_model import PlayerModel
from computer_player import  ComputerPlayer
from feedback_mechanism import Feedback
from logic import Logic
import json
from typing import Dict, List

class DeadAndInjuredCLIApp:
    def __init__(self, player: PlayerModel, opponent: PlayerModel | ComputerPlayer):
        self.player = player
        self.opponent = opponent
        self.logic = Logic()
        self.LEADERBOARD_FILE = '../leaderboard.json'

    def enter_and_verify_code(self, player_name: str, description='PIN') -> List[int]:
        code = input(f'{player_name}, enter Your 4 unique digit {description} (0 -9): ')
        validate_code = self.logic.validate_unique_code(code)
        return validate_code

    def get_player_pin (self, player_name: str) -> List[int]:
        return self.enter_and_verify_code(player_name, 'PIN')

    def get_player_guess(self, player_name) -> List[int]:
        return self.enter_and_verify_code(player_name,'GUESS')

    def initialize_player_pins(self):
        player_pin = self.get_player_pin(self.player.name.title())
        if not player_pin:
            print('Invalid pin entered')
            return False

        self.player.pin = player_pin
        print(f'{self.player.name.title()} has chosen a valid pin...\n')

        if not self.opponent.is_human:
            self.opponent.computer_pin()
            print(f'{self.opponent.name.title()} has generated a valid pin...\n')
            return True

        else:
            opponent_pin = self.get_player_pin(self.opponent.name.title())
            if not opponent_pin:
                print('Invalid pin entered\n')
                return False

            self.opponent.pin = opponent_pin
            print(f'{self.opponent.name.title()} has chosen a valid pin...\n')
            return True

    def simulate_player_guessing(self,player: PlayerModel | ComputerPlayer, opponent: PlayerModel | ComputerPlayer):

        player_guess = self.get_player_guess(player.name.title())
        if not player_guess:
            print('Invalid guess entered\n')
            return False

        player.guess = player_guess
        print(f'{player.name.title()} has guessed picked a guess...\n')

        player_feedback_data = self.logic.compare_pin_to_guess(player, opponent)
        if not player_feedback_data:
            print(f'A problem occurred comparing {player.name.title()} guess to {opponent.name.title()} pin')
            return False

        player.current_feedback = player_feedback_data
        print(player.current_feedback)

        player_feedback_message = Feedback(player_feedback_data).feedback_result()
        print(f'Feedback to {player.name.title()} after comparison is {player_feedback_message}')

        self.logic.update_feedback_history(player, feedback=player_feedback_message)
        print(player.feedback_history)

        if self.logic.has_won(player):
            self.logic.save_winner(self.LEADERBOARD_FILE,player)
            self.logic.rank_winner_by_guess_count(self.LEADERBOARD_FILE)
            return True
        return False

    def run_cli_game(self):
        entering_pin = True
        while entering_pin:
           if not self.initialize_player_pins():
               continue
           break

        #main guessing loop
        while True:
            if not self.simulate_player_guessing(player=self.player, opponent=self.opponent):
                pass
            else:
                break

            if not self.opponent.is_human:
                pass # the computer guessing strategy , breaks when the computer wins

            if not self.simulate_player_guessing(player=self.opponent, opponent=self.player):
                pass
            else:
                break


def creating_human_player() -> PlayerModel:
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

def create_player() -> Dict[str, PlayerModel | ComputerPlayer]:
    initial_prompt = input('Do you want to play again comp("y/n"): ').lower()
    if initial_prompt.startswith('y'):
        computer_player = ComputerPlayer()
        computer_player.is_human = False
        new_player = creating_human_player()
        return {'player': new_player, 'opponent': computer_player}
    else:
        player = creating_human_player()
        opponent = creating_human_player()
        return {'player': player, 'opponent': opponent}




if __name__ == '__main__':
   players = create_player()
   player_1 = players['player']
   player_2 = players['opponent']



   game_cli_app = DeadAndInjuredCLIApp(player_1, player_2)
   game_cli_app.run_cli_game()











