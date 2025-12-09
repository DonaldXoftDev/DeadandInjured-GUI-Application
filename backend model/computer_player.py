import random
from player_model import PlayerModel
from itertools import permutations


class ComputerPlayer(PlayerModel):
    def __init__(self):
        super().__init__(name='Computer')
        self.possible_pin_list = [list(item) for item in permutations(range(0, 10), 4)]

    def computer_pin(self):
        pin = random.choice(self.possible_pin_list)
        self.pin = pin
        return pin


    def computer_guess(self):
        self.guess.clear()
        comp_guess = random.choice(self.possible_pin_list)
        self.guess = comp_guess
        return comp_guess



