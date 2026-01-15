from enum import Enum, auto

class GameScreen(Enum):
    MODE_SELECT = auto()
    NAME_SETUP = auto()
    PIN_ENTRY = auto()
    GUESS_ENTRY = auto()
    STATS_SCREEN = auto()
    GAME_OVER = auto()

