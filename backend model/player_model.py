import json
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

    def validate_unique_code(self, input_string: str) -> List:
        clean_string = input_string.strip()
        if len(clean_string) != 4 or not clean_string.isdigit():
            return []

        if len(set(clean_string)) < 4:
            return []

        return [int(n) for n in clean_string]




















