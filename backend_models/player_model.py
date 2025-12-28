from logging import raiseExceptions
from typing import Dict, Optional


class PlayerModel:
    def __init__(self,name: Optional[str] = None):
        self.name = name
        self.pin: list[int] = []
        self.guess: list[int] = []
        self.guess_count = 0
        self.current_feedback: dict[str, int] = {}
        self.feedback_history: list[str] = []
        self.is_human = True

    def set_name(self, name: str):
        self.name = name

    def get_name(self):
        return self.name if self.name is not None else ''

    def update_pin(self,pin: list[int]):
        self.pin = pin


    def update_guess(self,guess: list[int]):
        self.guess = guess


    def update_feed_back_history (self, feedback: str):
        self.feedback_history.append(feedback)

    def update_current_feedback(self, data: dict[str, int]):
        self.current_feedback = data

    def increment_guess_count(self):
        self.guess_count += 1




















