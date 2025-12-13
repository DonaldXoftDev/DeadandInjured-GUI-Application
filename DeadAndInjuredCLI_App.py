from backend_models.player_model import PlayerModel
from backend_models.computer_player import ComputerPlayer
from backend_models.feedback_mechanism import  Feedback
from backend_models.logic import Logic
from cli_interface import Interface
from typing import Dict, List


class DeadAndInjuredCLIApp:
    def __init__(self):
        self.interface = Interface()
        self.all_players = self.create_players()
        self.player = self.all_players['player']
        self.opponent = self.all_players['opponent']
        self.logic = Logic()
        self.LEADERBOARD_FILE = 'leaderboard.json'

    def create_players(self) -> Dict[str, PlayerModel | ComputerPlayer]:
        is_comp_opponent = self.interface.play_with_comp_prompt()

        if is_comp_opponent.startswith('y'):
            computer = ComputerPlayer()
            computer.is_human = False
            self.interface.display_message('You are playing with computer...')
            player = PlayerModel(self.interface.get_player_name())
            self.interface.display_message(f'Player {player.name.title()} created...')
            return {'player': player, 'opponent': computer}
        else:
            player = PlayerModel(self.interface.get_player_name())
            self.interface.display_message(f'Player {player.name.title()} created...')
            opponent = PlayerModel(self.interface.get_player_name())
            self.interface.display_message(f'Player {opponent.name.title()} created...')
            return {'player': player, 'opponent': opponent}


    def enter_and_verify_code(self, player_name: str, description='PIN') -> List[int]:
        code = self.interface.get_code_input(player_name, description)
        validate_code = self.logic.validate_unique_code(code)
        return validate_code

    def get_verified_pin (self, player_name: str) -> List[int]:
        return self.enter_and_verify_code(player_name, 'PIN')

    def get_verified_guess(self, player_name) -> List[int]:
        return self.enter_and_verify_code(player_name,'GUESS')

    def initialize_player_pins(self):
        player_pin = self.get_verified_pin(self.player.name.title())
        if not player_pin:
            self.interface.display_error_message('Invalid pin entered.')
            return False

        self.player.pin = player_pin
        self.interface.display_message(f'{self.player.name.title()} has chosen a valid pin...')

        if not self.opponent.is_human:
            self.opponent.computer_pin()
            self.interface.display_message(f'{self.opponent.name.title()} has generated a valid pin...')
            return True

        else:
            opponent_pin = self.get_verified_pin(self.opponent.name.title())
            if not opponent_pin:
                self.interface.display_error_message('Invalid pin entered.')
                return False

            self.opponent.pin = opponent_pin
            self.interface.display_message(f'{self.opponent.name.title()} has chosen a valid pin...')
            return True

    def simulate_player_guessing(self,valid_guess: List[int],player: PlayerModel | ComputerPlayer,
                                 opponent: PlayerModel | ComputerPlayer):
        player.guess = valid_guess
        self.interface.display_message(f'{player.name.title()} has guessed...{player.guess}\n')

        player_feedback_data = self.logic.compare_pin_to_guess(player, opponent)
        self.interface.display_message(f'You are comparing your guess of {player.guess} to the opponent pin of {opponent.pin}')
        self.logic.update_guess_count(player)
        if not player_feedback_data:
            self.interface.display_error_message(f'A problem occurred comparing {player.name.title()} '
                                                 f'guess to {opponent.name.title()} pin')
            return False

        player.current_feedback = player_feedback_data

        player_feedback_message = Feedback(player_feedback_data).feedback_result()
        self.interface.display_message(f'Feedback to {player.name.title()}'
                                       f' after comparison is {player_feedback_message}')

        self.logic.update_feedback_history(player, feedback=player_feedback_message)

        if self.logic.has_won(player):
            self.interface.display_message(f'{player.name.title()} has won!')
            self.interface.display_message(f'Adding {player.name.title()} to the leaderboard...')
            self.logic.save_winner(self.LEADERBOARD_FILE,player)
            self.logic.rank_winner_by_guess_count(self.LEADERBOARD_FILE  )
            return True
        return False

    def computer_guessing_strategy(self) -> None:
        computer = self.opponent
        dummy_computer = ComputerPlayer()

        new_possible_list = []
        for poss_pin in computer.possible_pin_list:
            dummy_computer.pin = poss_pin

            temp_feedback_data = self.logic.compare_pin_to_guess(computer, dummy_computer)

            if (computer.current_feedback['dead'] == temp_feedback_data['dead']
                and computer.current_feedback['injured'] == temp_feedback_data['injured']):
                new_possible_list.append(poss_pin)

        computer.possible_pin_list = new_possible_list


    def handle_computer_turn(self):
        valid_guess = self.opponent.computer_guess()

        is_win = self.simulate_player_guessing(
            valid_guess=valid_guess,
            player=self.opponent,
            opponent=self.player
        )

        if is_win:
            return True

        self.computer_guessing_strategy()

        self.interface.display_message(f'possible list length is now: {len(self.opponent.possible_pin_list)}\n')
        return False

    def handle_player_turn(self, player: PlayerModel | ComputerPlayer, opponent: PlayerModel | ComputerPlayer) -> bool:
        valid_guess = self.get_verified_guess(player.name.title())

        if not valid_guess:
            self.interface.display_error_message('Invalid pin entered.\n')
            return False

        is_win = self.simulate_player_guessing(
            valid_guess=valid_guess,
            player=player,
            opponent=opponent
        )

        if is_win:
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
            #TODO: don't forget to handle the conflict of invalid pin and has not won
            if not self.handle_player_turn(player=self.player, opponent=self.opponent):
                pass
            else:
                break

            if not self.opponent.is_human:
                if not self.handle_computer_turn():
                    continue
                break
            else:
                if not self.handle_player_turn(player=self.opponent, opponent=self.opponent):
                    continue
                else:
                    break


if __name__ == '__main__':
   game_cli_app = DeadAndInjuredCLIApp()
   game_cli_app.run_cli_game()











