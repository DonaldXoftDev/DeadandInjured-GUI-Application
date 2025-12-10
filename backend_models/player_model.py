from typing import List, Dict


class PlayerModel:
    def __init__(self,name):
        self.name = name
        self.pin = []
        self.guess = []
        self.guess_count = 0
        self.current_guess: List = []
        self.current_feedback: Dict = {}
        self.feedback_history = []
        self.is_human = True



















