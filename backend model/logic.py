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
    def validate_unique_code(self, input_string: str) -> List:
        clean_string = input_string.strip()
        if len(clean_string) != 4 or not clean_string.isdigit():
            return []

        if len(set(clean_string)) < 4:
            return []

        return [int(n) for n in clean_string]



    def compare_pin_to_guess(self,player: PlayerModel, opponent: PlayerModel) -> Dict:
        if not player.guess or not opponent.pin:
            return {}

        dead = 0
        for _, (num_a, num_b) in enumerate(zip(player.guess, opponent.pin)):
            if num_a == num_b:
                dead += 1

        total_shared_digit = len(set(player.guess).intersection(opponent.pin))
        inj = total_shared_digit - dead
        player.guess_count += 1

        return {'dead': dead, 'injured': inj}

    def update_feedback_history(self, player: PlayerModel, feedback: str) -> bool:
        player.feedback_history.append(feedback)
        return True


    def has_won(self, player: PlayerModel) -> bool:
        if player.current_feedback.get('dead') == 4 or player.current_feedback.get('injured') == 4:
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
                    record_list =  []

                match_found = False
                for record in record_list:
                    if record['name'] == winner.name:
                        record['guess_count'] = winner.guess_count
                        match_found = True

                if not match_found:
                    record_list.append(new_data)

        except (FileNotFoundError, JSONDecodeError):
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





