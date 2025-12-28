from typing import Protocol, AnyStr

from backend_models.computer_player import ComputerPlayer
from backend_models.player_model import PlayerModel
from backend_models.logic import Logic
from backend_models.main_game_model import  MainGameModel


class StatDetails:
    def __init__(self, turn: PlayerModel):
        self.player_name:str = turn.name.capitalize()
        self.player_pin: list[int] = turn.pin
        self.player_guess: list[int] = turn.guess
        self.all_player_stats: list[StatDetails]
        self.player_guess_count: int = turn.guess_count
        self.feedback_history: list[str] = turn.feedback_history


class ViewProtocol(Protocol):
    def render_new_screen(self, details: StatDetails | str | None = None):
        ...

    def display_error_popup(self, message):
        ...

    def start(self):
        ...


class GamePresenter:
    def __init__(self, view: ViewProtocol, logic:Logic, game_model:MainGameModel):
        self.view = view
        self.Logic = logic
        self.game_model = game_model


    def get_next_player(self) -> PlayerModel:
        next_index = (self.game_model.current_index + 1) % len(self.game_model.players)
        self.game_model.current_index = next_index
        return self.game_model.players[self.game_model.current_index]



    def create_players(self,mode) -> bool:
        if mode.lower() == 'h_vs_c':
            computer = ComputerPlayer()
            computer.set_as_comp()
            human_player = PlayerModel()
            self.game_model.players.extend([human_player, computer])
        else:
            self.game_model.players.extend([PlayerModel() for _ in range(2)])

        return True

    def create_player_sequence(self, mode: str):
        if self.create_players(mode):
            self.game_model.current_screen = 'NAME_SETUP'
            self.view.render_new_screen()
        else:
            pass


    def store_name_sequence(self, name: str):
        if not name:
            msg = 'The name cannot be empty.'
            self.view.display_error_popup(msg)

        elif len(name) < 3:
            msg = 'The player name is too short'
            self.view.display_error_popup(msg)

        else:
            if self.game_model.screen_turn == 0:
                self.game_model.current_player = self.game_model.players[0]
                self.game_model.current_player.name = name
            else:
                self.game_model.current_player = self.get_next_player()
                self.game_model.current_player.name = name

            self.game_model.screen_turn += 1

            if self.game_model.screen_turn < len(self.game_model.players) and self.game_model.players[1].is_human:
                self.game_model.current_screen = 'NAME_ENTRY'
                self.view.render_new_screen()
            else:
                self.game_model.screen_turn = 0
                self.game_model.current_screen = 'PIN_ENTRY'
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                self.view.render_new_screen(detail)




    def pin_submitted_sequence(self, pin: str):
        pin = pin.strip()
        if not pin:
            msg = 'The PIN cannot be empty.'
            self.view.display_error_popup(msg)

        elif not  self.Logic.is_unique(pin):
            msg = 'The PIN is not unique.'
            self.view.display_error_popup(msg)

        elif not self.Logic.is_all_digit(pin):
            msg = 'The PIN has to be all digits.'
            self.view.display_error_popup(msg)
        else:
            valid_pin = self.Logic.parse_code_as_list(pin)
            self.game_model.current_player.update_pin(valid_pin)

            self.game_model.screen_turn += 1

            if self.game_model.screen_turn < len(self.game_model.players) and self.game_model.players[1].is_human:
                self.game_model.current_screen = 'PIN_ENTRY'
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                self.view.render_new_screen(detail)
            else:
                self.game_model.screen_turn = 0
                self.game_model.current_screen = 'GUESS_ENTRY'
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                self.view.render_new_screen(detail)




    def guess_submitted_sequence(self, guess: str):
        guess = guess.strip()
        if not guess:
            msg = 'The PIN cannot be empty.'
            self.view.display_error_popup(msg)

        elif not self.Logic.is_unique(guess):
            msg = 'The PIN is not unique.'
            self.view.display_error_popup(msg)

        elif not self.Logic.is_all_digit(guess):
            msg = 'The PIN has to be all digits.'
            self.view.display_error_popup(msg)
        else:
            valid_guess = self.Logic.parse_code_as_list(guess)
            self.game_model.current_player.update_guess(valid_guess)

    def guess_again_sequence(self):
        ...

