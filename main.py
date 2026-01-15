from game_presenter import GamePresenter
from frontend_model.game_view import GameView
from backend_models.game_data_model import MainGameModel

from backend_models.logic import Logic


logic = Logic()
model = MainGameModel()
view = GameView(model)
presenter = GamePresenter(view=view, logic=logic, game_model=model)
view.presenter = presenter
presenter.view.start()