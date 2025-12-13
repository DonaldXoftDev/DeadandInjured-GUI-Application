from json import JSONDecodeError

from prettytable import PrettyTable
import random



from backend_models.player_model import PlayerModel
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

        return {'dead': dead, 'injured': inj}

    def update_feedback_history(self, player: PlayerModel, feedback: str) -> bool:
        player.feedback_history.append(feedback)
        return True

    def update_guess_count(self, player: PlayerModel) -> None:
        player.guess_count += 1


    def has_won(self, player: PlayerModel) -> bool:
        if player.current_feedback.get('dead') == 4 or player.current_feedback.get('injured') == 4:
            return True
        return False


    def save_winner(self, file_name: str, winner: PlayerModel) -> None:
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


    def rank_winner_by_guess_count(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='utf-8') as f:
                loaded_user_record = json.load(f)

            sorted_by_guess_count = sorted(loaded_user_record, key=lambda x: x['guess_count'])

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(sorted_by_guess_count, f, indent=4)


        except FileNotFoundError:
            print(f'{file_name} not found to induce the ranking functionality')





