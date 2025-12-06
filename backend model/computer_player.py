import random
from player import Player
from itertools import permutations


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__(name='Computer')
        self.possible_pin_list = [list(item) for item in permutations(range(0, 10), 4)]

    def computer_pin(self):
        self.pin.clear()
        computer_pin = random.choice(self.possible_pin_list)
        self.pin.append(random.choice(computer_pin))
        return computer_pin

    def computer_guess(self):
        self.guess.clear()
        computer_guess = random.choice(self.possible_pin_list)
        self.guess.append(computer_guess)
        return computer_guess

    def computer_guessing_strategy(self, pin):
        self.guess = self.computer_guess()
        print(self.guess.copy())
        feedback_dead, feedback_inj= self.compare_guesses(pin)

        for possible_pin in self.possible_pin_list:
            possible_dead, possible_inj= self.compare_guesses(possible_pin)
            if feedback_dead == possible_dead and feedback_inj == possible_inj:
                continue
            else:
                self.possible_pin_list.remove(possible_pin)


computer = ComputerPlayer()
user_pin = [8, 1, 2, 3]
computer.computer_guessing_strategy(user_pin)
print(computer.display_feedback_message())



