from typing import Protocol
from backend_models.computer_player import ComputerPlayer
from backend_models.feedback_mechanism import Feedback
from backend_models.game_screen_model import GameScreen
from backend_models.player_model import PlayerModel
from backend_models.logic import Logic
from backend_models.game_data_model import  MainGameModel
from backend_models.stats_model import StatDetails
from backend_models.gameover_data_model import GameOverDetails
from backend_models.view_model import AppViewModel


class ViewProtocol(Protocol):
    def render_new_screen(self, vm: AppViewModel) -> None:
        ...

    def display_error_popup(self,label: str, message: str):
        ...

    def start(self):
        ...


class GamePresenter:
    def __init__(self, view: ViewProtocol, logic:Logic, game_model:MainGameModel):
        self.view = view
        self.Logic = logic
        self.game_model = game_model
        self.base_game_player = PlayerModel()
        self.base_game_player.set_name('GAME-STATS')
        self.master_stats = StatDetails(self.base_game_player)
        self.file_name = 'D_n_I_leaderboard.json'


    def get_next_player(self) -> PlayerModel:
        next_index = self.get_next_index()
        self.game_model.current_index = next_index
        return self.game_model.players[self.game_model.current_index]

    def get_next_index(self) -> int:
        return  (self.game_model.current_index + 1) % len(self.game_model.players)

    def create_players(self,mode) -> bool:
        if mode.lower() == 'h_vs_c':
            computer = ComputerPlayer()
            computer.set_as_comp()
            human_player = PlayerModel()
            self.game_model.players.clear()
            self.game_model.players.extend([human_player, computer])
        else:
            self.game_model.players.extend([PlayerModel() for _ in range(2)])

        return True

    def create_player_sequence(self, mode: str):
        if self.create_players(mode):
            self.game_model.current_screen = GameScreen.NAME_SETUP
            vm = AppViewModel(GameScreen.NAME_SETUP)
            self.view.render_new_screen(vm)
        else:
            pass


    def store_name_sequence(self, name: str):
        label = 'NAME'
        if not name:
            print('NO name is stored')
            msg = 'The name cannot be empty.'
            self.view.display_error_popup(label,msg)

        elif len(name) < 2:
            msg = 'The player name is too short'
            self.view.display_error_popup(label, msg)

        else:
            if self.game_model.screen_turn == 0:
                self.game_model.current_player = self.game_model.players[0]
                self.game_model.current_player.set_name(name)
            else:
                self.game_model.current_player = self.get_next_player()
                self.game_model.current_player.set_name(name)

            self.game_model.screen_turn += 1

            if self.game_model.screen_turn < len(self.game_model.players) and all(p.is_human for p in self.game_model.players):
                self.game_model.current_screen = GameScreen.NAME_SETUP
                vm = AppViewModel(GameScreen.NAME_SETUP)
                self.view.render_new_screen(vm)

            else:
                self.game_model.screen_turn = 0
                self.game_model.current_screen = GameScreen.PIN_ENTRY
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                vm = AppViewModel(GameScreen.PIN_ENTRY, detail)
                self.view.render_new_screen(vm)


    def pin_submitted_sequence(self, pin: str):
        pin = pin.strip()
        print(pin)
        label= 'PIN'
        if not pin:
            msg = 'The PIN cannot be empty.'
            self.view.display_error_popup(label, msg)

        elif not self.Logic.is_unique(pin):
            msg = 'The PIN is not unique.'
            self.view.display_error_popup(label, msg)

        elif not self.Logic.is_all_digit(pin):
            msg = 'The PIN has to be all digits.'
            self.view.display_error_popup(label, msg)
        else:
            valid_pin = self.Logic.parse_code_as_list(pin)
            self.game_model.current_player.update_pin(valid_pin)

            self.game_model.screen_turn += 1

            if self.game_model.screen_turn < len(self.game_model.players) and all(p.is_human for p in self.game_model.players):
                self.game_model.current_screen = GameScreen.PIN_ENTRY
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                vm = AppViewModel(GameScreen.PIN_ENTRY, detail)
                self.view.render_new_screen(vm)
            else:
                self.game_model.screen_turn = 0
                self.game_model.current_screen = GameScreen.GUESS_ENTRY
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                vm = AppViewModel(GameScreen.GUESS_ENTRY, detail)
                self.view.render_new_screen(vm)


    def guess_submitted_sequence(self, guess: str):
        guess = guess.strip()
        label = 'GUESS'
        if not guess:
            msg = 'The PIN cannot be empty.'
            self.view.display_error_popup(label, msg)

        elif not self.Logic.is_unique(guess):
            msg = 'The PIN must be 4 digits and unique.'
            self.view.display_error_popup(label, msg)

        elif not self.Logic.is_all_digit(guess):
            msg = 'The PIN has to be all digits.'
            self.view.display_error_popup(label, msg)
        else:
            valid_guess = self.Logic.parse_code_as_list(guess)

            player = self.game_model.current_player
            opponent = self.game_model.players[self.get_next_index()]

            #updates the current player's guess
            player.update_guess(valid_guess)
            player.increment_guess_count()

            #returns the result of the comparison of player guess and opponent pin as a dict
            feedback_data = self.Logic.compare_pin_to_guess(player, opponent)

            if not player.is_human:
                print('the player is computer')
                self.Logic.computer_guessing_strategy(computer=player)

            print('definitely a human playing!')
            # updates the player's feedback
            player.update_current_feedback(feedback_data)

            #returns a string of the feedback message e.g. 1d 2inj
            feedback_msg = Feedback(feedback_data).feedback_result()
            player.update_feed_back_history(feedback_msg)

            if self.Logic.has_won(player):
                self.game_model.current_screen = GameScreen.GAME_OVER
                game_over_details = GameOverDetails(winner=player, loser=opponent)
                print('wow, shocked you won!')
                self.Logic.save_winner(self.file_name, winner=player)
                self.Logic.rank_winner_by_guess_count(self.file_name)
                vm = AppViewModel(GameScreen.GAME_OVER, game_over_details)
                self.view.render_new_screen(vm)

            else:
                self.game_model.current_screen = GameScreen.STATS_SCREEN
                stats_details = StatDetails(player)

                sub_stats = self.master_stats.sub_stats
                sub_stat_names = [p.player_name for p in sub_stats]

                if player.name in sub_stat_names:
                    matched_stat = None
                    for stat in sub_stats:
                        if stat.player_name == player.name:
                            matched_stat = stat
                            break
                    matched_stat.player_guess = player.guess
                    matched_stat.player_guess_count = player.guess_count
                    matched_stat.feedback_history = player.feedback_history

                else:
                    sub_stats.append(stats_details)

                vm = AppViewModel(GameScreen.STATS_SCREEN, self.master_stats)
                self.view.render_new_screen(vm)
                print('This should happen')


    def guess_again_sequence(self):
        self.game_model.current_screen = GameScreen.GUESS_ENTRY
        self.game_model.current_player = self.get_next_player()
        detail = StatDetails(self.game_model.current_player)
        vm = AppViewModel(GameScreen.GUESS_ENTRY, detail)
        self.view.render_new_screen(vm)
