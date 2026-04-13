"""
The Presenter module in the Model-View-Presenter (MVP) architecture.
This acts as the central coordinator, reacting to user inputs from the View,
updating the underlying Game Models, and instructing the View to render updates.
"""
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
    """
    A structural type protocol defining the expected interface of the View.
    This allows the Presenter to remain decoupled from the concrete Tkinter GUI,
    facilitating easier testing and strict separation of concerns.
    """
    def render_new_screen(self, vm: AppViewModel) -> None:
        """Transitions the application to a new screen based on the provided View Model."""
        ...

    def display_error_popup(self,label: str, message: str):
        """Renders an error modal/popup to the user."""
        ...
    def reset_ui_state(self):
        ...
    def start(self):
        """Starts the main UI event loop."""
        ...


class GamePresenter:
    """
    Orchestrates the Dead and Injured game flow.
    
    Responsibilities:
    - Managing the turn-based state machine.
    - Handling data validation for user inputs (Names, PINs, Guesses).
    - Facilitating communication between the Logic/Model layers and the View layer.
    """
    def __init__(self, view: ViewProtocol, logic:Logic, game_model:MainGameModel):
        """
        Initializes the presenter with its required dependencies.
        """
        self.mode = None
        self.view = view
        self.Logic = logic
        self.game_model = game_model
        self.max_screen_turn = 2
        
        # Base player object used solely to aggregate and display global match statistics
        self.base_game_player = PlayerModel()
        self.base_game_player.set_name('GAME-STATS')
        self.master_stats = StatDetails(self.base_game_player)
        
        # Local file reference for persisting leaderboard statistics
        self.file_name = 'D_n_I_leaderboard.json'


    def get_next_player(self) -> PlayerModel:
        """Advances the internal turn index and returns the player whose turn is next."""
        next_index = self.get_next_turn()
        self.game_model.current_index = next_index
        return self.game_model.players[self.game_model.current_index]

    def get_next_turn(self) -> int:
        """Calculates the next player's index using modulo arithmetic for circular looping."""
        return  (self.game_model.current_index + 1) % len(self.game_model.players)

    def create_players(self,mode) -> bool:
        """
        Instantiates the required PlayerModel objects based on the selected game mode.
        
        Args:
            mode (str): The chosen game mode (e.g., 'H_Vs_C' or 'H_Vs_H').
        Returns:
            bool: True indicating successful creation.
        """
        self.mode = mode
        if self.mode.lower() == 'h_vs_c':
            computer = ComputerPlayer()
            computer.set_as_comp()
            human_player = PlayerModel()
            self.game_model.players.clear()
            self.game_model.players = [human_player, computer]

        elif self.mode.lower() == 'h_vs_h':
            self.game_model.players = [PlayerModel() for _ in range(2)]
        else:
            print('Something went wrong while creating players')

        return True

    def create_player_sequence(self, mode: str):
        """
        Triggered when a user selects a game mode from the home screen.
        Initializes players and commands the view to transition to the Name Setup screen.
        
        Args:
            mode (str): The chosen game mode.
        """
        self.mode = mode
        if self.create_players(self.mode):
            self.game_model.current_screen = GameScreen.NAME_SETUP
            vm = AppViewModel(GameScreen.NAME_SETUP)
            self.view.render_new_screen(vm)

    def validate_and_store_name(self,name):
        label = 'NAME'
        if not name:
            print('NO name is stored')
            msg = 'The name cannot be empty.'
            self.view.display_error_popup(label, msg)

        elif len(name) < 2:
            msg = 'The player name is too short'
            self.view.display_error_popup(label, msg)

        else:
            self.game_model.current_player = self.get_next_player()
            self.game_model.current_player.set_name(name)
            print(type(self.game_model.current_player))

    def store_name_sequence(self, name: str):
        """
        Validates and registers a player's name.
        It continuously prompts the Name Setup screen until all human players are named,
        after which it transitions to the PIN Entry screen.
        
        Args:
            name (str): The submitted player name.
        """
        if self.mode.lower() == 'h_vs_h':
            self.validate_and_store_name(name)

            self.game_model.screen_turn += 1

            # If there are more human players left to name, reload Name Setup
            if self.game_model.screen_turn != self.max_screen_turn:
                self.game_model.current_screen = GameScreen.NAME_SETUP
                vm = AppViewModel(GameScreen.NAME_SETUP)
                self.view.render_new_screen(vm)

            else:
                # Setup complete. Reset turn counter and proceed to PIN setup phase
                self.game_model.screen_turn = 0
                self.game_model.current_player = self.get_next_player()
        else:
            self.validate_and_store_name(name)

        self.game_model.current_screen = GameScreen.PIN_ENTRY
        detail = StatDetails(self.game_model.current_player)
        vm = AppViewModel(GameScreen.PIN_ENTRY, detail)
        self.view.render_new_screen(vm)

    def validate_and_store_digits(self, digits: str, label: str):
        """
        Validates numeric code strings for standard rules (PINs and Guesses).
        Displays a tailored error popup if constraints are violated.
        
        Args:
            digits (str): The code string to validate.
            label (str): The context of the input ('PIN' or 'GUESS').
        Returns:
            bool: True if an error is present, False if the input is completely valid.
        """
        if not digits:
            msg = f'The {label} cannot be empty.'
            self.view.display_error_popup(label, msg)


        elif not self.Logic.is_unique(digits):
            msg = f'The {label} must be 4 digits and unique.'
            self.view.display_error_popup(label, msg)


        elif not self.Logic.is_all_digit(digits):
            msg = f'The {label} has to be all digits.'
            self.view.display_error_popup(label, msg)

        else:
            valid_pin = self.Logic.parse_code_as_list(digits)
            self.game_model.current_player.update_pin(valid_pin)

    def pin_submitted_sequence(self, pin: str):
        """
        Validates and registers a player's secret PIN.
        Transitions to the next player's PIN entry, or proceeds to the guessing phase
        if all players have successfully entered their PINs.
        """
        pin = pin.strip()
        label= 'PIN'

        # Proceed only if the input passes all validation checks
        if self.mode == 'h_vs_h':
            self.validate_and_store_digits(digits=pin, label=label)

            self.game_model.screen_turn += 1

            # Check if there are still human players needing to set a PIN
            if self.max_screen_turn != 2:
                self.game_model.current_screen = GameScreen.PIN_ENTRY
                self.game_model.current_player = self.get_next_player()
                detail = StatDetails(self.game_model.current_player)
                vm = AppViewModel(GameScreen.PIN_ENTRY, detail)
                self.view.render_new_screen(vm)
            else:
                # Setup phase entirely complete, initiate main guessing loop
                self.game_model.screen_turn = 0
                self.game_model.current_player = self.get_next_player()
        else:
            #tell the view to render the comp screen saying that it has chosen it's pin and after 3s remove it
            computer = self.game_model.players[self.get_next_turn()]
            if isinstance(computer, ComputerPlayer):
                computer.computer_pin()
            else:
                self.validate_and_store_digits(digits=pin, label=label)


        self.game_model.current_screen = GameScreen.GUESS_ENTRY
        detail = StatDetails(self.game_model.current_player)
        vm = AppViewModel(GameScreen.GUESS_ENTRY, detail)
        self.view.render_new_screen(vm)


    def guess_submitted_sequence(self, guess: str):
        """
        The core game loop sequence triggered when a user submits a guess.
        Processes the guess, calculates feedback, checks for win conditions,
        updates local player metrics, and determines if the game should end
        or proceed to the inter-turn Stats screen.
        """
        guess = guess.strip()
        label = 'GUESS'
        
        # Do nothing if the validation flags an error
        if  self.validate_and_store_digits(guess, label):
            pass
        else:
            # Parse the input into a usable integer list
            valid_guess = self.Logic.parse_code_as_list(guess)

            player = self.game_model.current_player
            opponent = self.game_model.players[self.get_next_turn()]
            print(player.guess , opponent.pin)
            print(player.pin)


            # Update the current player's state tracking
            player.update_guess(valid_guess)
            player.increment_guess_count()
            print(player.name, opponent.name)

            # Execute core rules engine: Evaluate guess vs opponent's PIN
            feedback_data = self.Logic.compare_pin_to_guess(player, opponent)
            print(feedback_data)

            # If it's a computer turn, allow it to filter its internal logic branches
            if not player.is_human:
                self.Logic.computer_guessing_strategy(computer=player)

            # Store raw mathematical feedback internally
            player.update_current_feedback(feedback_data)

            # Construct user-facing string representation of feedback (e.g., '1d 2inj')
            feedback = Feedback(feedback_data)
            feedback_msg = feedback.feedback_result()
            history_item = feedback.structure_feedback_msg(current_guess=valid_guess, feedback_msg=feedback_msg)

            # Append turn history for the stats screen
            player.update_feed_back_history(history_item)

            # -- Win Condition Check --
            if self.Logic.has_won(player):
                self.game_model.current_screen = GameScreen.GAME_OVER
                game_over_details = GameOverDetails(winner=player, loser=opponent)
                
                # Persist match data and trigger UI render
                self.Logic.save_to_leaderboard(self.file_name, winner=player, loser=opponent)
                vm = AppViewModel(GameScreen.GAME_OVER, game_over_details)
                self.view.render_new_screen(vm)

            else:
                # Round is over but game continues. Show the intermediary Stats Screen.
                self.game_model.current_screen = GameScreen.STATS_SCREEN
                stats_details = StatDetails(player)

                # Update the presenter's central stats aggregate tracking
                sub_stats = self.master_stats.sub_stats
                sub_stat_names = [p.player_name for p in sub_stats]

                if player.name in sub_stat_names:
                    # Update existing record
                    matched_stat = None
                    for stat in sub_stats:
                        if stat.player_name == player.name:
                            matched_stat = stat
                            break
                    matched_stat.player_guess = player.guess
                    matched_stat.player_guess_count = player.guess_count
                    matched_stat.feedback_history = player.feedback_history

                else:
                    # Append new tracker if the player hasn't guessed yet
                    sub_stats.append(stats_details)

                vm = AppViewModel(GameScreen.STATS_SCREEN, self.master_stats)
                self.view.render_new_screen(vm)

    def leaderboard_sequence(self):
        """Stub for future implementation of fetching and displaying Leaderboard records."""
        sorted_leaderboard = self.Logic.get_sorted_leaderboard(self.file_name)
        vm = AppViewModel(GameScreen.LEADERBOARD, data=sorted_leaderboard)
        self.view.render_new_screen(vm)



    def guess_again_sequence(self):
        """Transitions from the inter-turn Stats Screen back to the main Guessing Screen for the next turn."""
        self.game_model.current_screen = GameScreen.GUESS_ENTRY
        self.game_model.current_player = self.get_next_player()
        detail = StatDetails(self.game_model.current_player)
        vm = AppViewModel(GameScreen.GUESS_ENTRY, detail)
        self.view.render_new_screen(vm)

    def reset_master_stats(self):
        self.base_game_player = PlayerModel()
        self.base_game_player.set_name('GAME-STATS')
        self.master_stats = StatDetails(self.base_game_player)

    def reset_sequence(self):
        #resets the main game data for the models
        self.game_model.reset_data()

        # reset the master stats
        self.reset_master_stats()

        #resets the data for the ui
        self.view.reset_ui_state()

        vm = AppViewModel(self.game_model.current_screen)
        self.view.render_new_screen(vm)
