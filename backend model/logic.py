from json import JSONDecodeError
from unittest.util import sorted_list_difference

from prettytable import PrettyTable
import random

def compare_pin_to_guess(g_list, p_list, name='computer') -> dict:
    if not g_list or not p_list:
        return {}

    dead = 0

    remaining_guess = []

    for i in range(len(g_list)):
        if g_list[i] == p_list[i]:
            dead += 1

        else:
            remaining_guess.append(g_list[i])

    total_shared_digits = len(set(g_list).intersection(set(p_list)))
    inj = total_shared_digits - dead

    return {'dead': dead, 'inj': inj, 'name': name}


# phase 5
# computer's guessing strategy
def computer_guessing_strategy(previous_pins:list, last_guess:list, last_result:dict) -> list:
    if not previous_pins:
        return []

    new_possible_pins = []
    for candidate_pin in previous_pins:
        test_result = compare_pin_to_guess(last_guess, candidate_pin, 'computer')

        if (last_result['dead'] == test_result['dead'] and
                last_result['inj'] == test_result['inj']):
            new_possible_pins.append(candidate_pin)


    return new_possible_pins

def computer_generate_pin():
    return random.sample(range( 10), 4)

def format_list_to_string(list_input):
    return "".join(str(n) for n in list_input)


# Structure feedbacks in a table
def generate_feedback_table(row_list, name='computer'):
    table = PrettyTable()
    table.field_names = [f'{name.title()} guess',f'Feedback to {name.title()}']

    for r in row_list:
        table.add_row(r)
    return table


from player_model import PlayerModel
import json
from typing import List, Dict

class Logic:
    def compare_pin_to_guess(self,player: PlayerModel, opponent: PlayerModel) -> Dict:

        dead = 0
        for _, (num_a, num_b) in enumerate(zip(player.guess, opponent.pin)):
            if num_a == num_b:
                dead += 1

        total_shared_digit = len(set(player.guess).intersection(opponent.pin))
        inj = total_shared_digit - dead
        player.guess_count += 1

        return {'dead': dead, 'injured': inj}

    def update_feedback_history(self, player: PlayerModel, feedback: str) -> None:
        return player.feedback_history.append(feedback)

    def has_won(self, player: PlayerModel, ) -> bool:
        if player.current_feedback['dead'] == 4 and player.current_feedback['injured'] == 4:
            return True
        return False


    def save_winner(self, file_name: str, winner: PlayerModel):
        new_data = {
            'name': winner.name,
            'guess_count': winner.guess_count,
        }

        record_list = []
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                record_list = json.load(f)

                if not isinstance(record_list, list):
                    return []

                match_found = False
                for record in record_list:
                    if record['name'] == winner.name:
                        record['guess_count'] = winner.guess_count
                        match_found = True

                if not match_found:
                    record_list.append(new_data)

        except FileNotFoundError:
            with open(file_name, 'w', encoding='utf-8') as f:
                initial_data =  [new_data]

                json.dump(initial_data, f, indent=4)

        except JSONDecodeError:
            record_list = [new_data]

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(record_list, f, indent=4)


    def rank_winner_by_guess_count(self, file_name: str):
        try:

            with open(file_name, 'r', encoding='utf-8') as f:
                loaded_user_record = json.load(f)

            sorted_by_guess_count = sorted(loaded_user_record, key=lambda x: x['guess_count'])

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(sorted_by_guess_count, f, indent=4)


        except FileNotFoundError:
            print(f'{file_name} not found to induce the ranking functionality')

player_1 = PlayerModel('Donald')
player_2 = PlayerModel('James')
player_3 = PlayerModel('John')

player_1.current_feedback = {'dead': 2, 'injured': 1}
player_2.current_feedback = {'dead': 3, 'injured': 1}
player_3.current_feedback = {'dead': 4, 'injured': 1}

player_1.guess_count += 2
player_2.guess_count += 0
player_3.guess_count += 8
logic = Logic()

LEADERBOARD_FILE = '../Leaderboard.json'
logic.save_winner(LEADERBOARD_FILE, player_1)
logic.save_winner(LEADERBOARD_FILE, player_2)
logic.save_winner(LEADERBOARD_FILE, player_3)
logic.rank_winner_by_guess_count(LEADERBOARD_FILE)



