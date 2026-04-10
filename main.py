"""
Entry point for the Dead and Injured GUI application.
Initializes the MVC components (Model, View, Presenter) and starts the main application loop.
"""
from game_presenter import GamePresenter
from frontend_model.game_view import GameView
from backend_models.game_data_model import MainGameModel

from backend_models.logic import Logic


# The utility functions of the game (handles the core rules and evaluation)
logic = Logic()

# The memory management model of the current game once initiated (stores state)
model = MainGameModel()

# The graphical user interface of the game
view = GameView(model)

# The controller of the game, acting as a coordinator bridging the model, logic, and view
presenter = GamePresenter(view=view, logic=logic, game_model=model)
view.presenter = presenter

# The literal start button for the game that kicks off the Tkinter main loop
presenter.view.start()
