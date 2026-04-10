from json import JSONDecodeError

from backend_models.computer_player import ComputerPlayer
from backend_models.player_model import PlayerModel
import json
from typing import List, Dict

class Logic:
    """
    Handles the core game logic and rules for the Dead and Injured game.
    """

    def validate_unique_code(self, input_string: str) -> List:
        """
        Validates that the input string is a 4-digit unique code.
        Returns a list of integers if valid, otherwise an empty list.
        """
        clean_string = input_string.strip()
        # Check if the length is exactly 4 and consists of only digits
        if len(clean_string) != 4 or not self.is_all_digit(clean_string):
            return []

        # Check if all characters in the string are unique
        if not self.is_unique(input_string):
            return []

        # Convert the string into a list of integers
        return [int(n) for n in clean_string]

    def parse_code_as_list(self,input_str):
        """
        Parses a string of digits into a list of integers.
        """
        clean_string = input_str.strip()
        return [int(n) for n in clean_string]

    def is_unique(self,code: str) -> bool:
        """
        Checks if the given string contains exactly 4 unique characters.
        """
        clean_string = code.strip()
        return len(set(clean_string)) == 4

    def is_all_digit(self, code:str) -> bool:
        """
        Checks if the given string consists only of digits.
        """
        clean_string = code.strip()
        return clean_string.isdigit()

    def compare_pin_to_guess(self,player: PlayerModel, opponent: PlayerModel) -> Dict:
        """
        Compares the player's guess against the opponent's pin.
        Calculates the number of 'dead' (correct digit, correct position) and
        'injured' (correct digit, wrong position) matches.
        """
        if not player.guess or not opponent.pin:
            return {}

        dead = 0
        # Calculate 'dead' matches (exact positional match)
        for _, (num_a, num_b) in enumerate(zip(player.guess, opponent.pin)):
            if num_a == num_b:
                dead += 1

        # Calculate total shared digits regardless of position
        total_shared_digit = len(set(player.guess).intersection(opponent.pin))
        
        # 'injured' matches are shared digits minus the ones that are already 'dead'
        inj = total_shared_digit - dead

        return {'dead': dead, 'injured': inj}

    def update_feedback_history(self, player: PlayerModel, feedback: str) -> bool:
        """
        Appends the feedback to the player's history.
        """
        player.feedback_history.append(feedback)
        return True

    def update_guess_count(self, player: PlayerModel) -> None:
        """
        Increments the player's guess count by 1.
        """
        player.guess_count += 1

    def has_won(self, player: PlayerModel) -> bool:
        """
        Checks if the player has won the game.
        A win is achieved when there are 4 'dead' matches.
        """
        # A player wins if they guess all 4 digits in the correct position ('dead' = 4).
        # Note: Checking for 'injured' = 4 might be a logical flaw depending on game rules.
        if player.current_feedback.get('dead') == 4:
            return True
        return False

    def save_to_leaderboard(self, file_name: str, winner: PlayerModel, loser: PlayerModel) -> None:
        """
        Saves/updates a match record using a dictionary structure for efficient O(1) lookups.
        This function's sole responsibility is to persist data.
        """
        # A normalized key ensures "Player1:Player2" is the same match as "player1:player2".
        match_key = f"{winner.name.lower()}:{loser.name.lower()}"
        new_data = {
            'winner': winner.name,
            'loser': loser.name,
            'winner_guess_count': winner.guess_count,
        }

        records_dict = {}
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                records_dict = json.load(f)
            
            # Backward compatibility: on-the-fly migration from old list format to new dict format.
            if isinstance(records_dict, list):
                old_list = records_dict
                records_dict = {}
                for record in old_list:
                    if 'winner' in record and 'loser' in record:
                        old_key = f'{record.get("winner", "").lower()}:{record.get("loser", "").lower()}'
                        records_dict[old_key] = record
        except (FileNotFoundError, JSONDecodeError):
            # If file is missing or corrupt, start with a new dictionary.
            pass

        # Update or create the record. The dictionary handles this in one step.
        records_dict[match_key] = new_data

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(records_dict, f, indent=4)

    def get_sorted_leaderboard(self, file_name: str) -> list:
        """
        Reads leaderboard data and returns it as a list sorted by guess count.
        This function's sole responsibility is to prepare data for display; it does not write to the file.
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                records_data = json.load(f)
            
            # Extract records for sorting, whether the file is the new dict or old list format.
            if isinstance(records_data, dict):
                list_to_sort = list(records_data.values())
            elif isinstance(records_data, list):
                list_to_sort = records_data
            else:
                return []

            # Sort by guess count. Using .get() with a default prevents errors on malformed records.
            return sorted(list_to_sort, key=lambda x: x.get('winner_guess_count', float('inf')))

        except (FileNotFoundError, JSONDecodeError):
            # If file doesn't exist or is corrupt, return an empty list for the UI.
            return []


    def computer_guessing_strategy(self, computer: PlayerModel) -> None:
        """
        Filters the computer's list of possible pins based on the feedback from the previous guess.
        Keeps only the pins that would yield the same feedback against the previous guess.
        """
        dummy_computer = ComputerPlayer()

        new_possible_list = []
        for poss_pin in computer.possible_pin_list:
            dummy_computer.pin = poss_pin

            # Compare the computer's last guess with this possible pin
            temp_feedback_data =  self.compare_pin_to_guess(computer, dummy_computer)

            # If the feedback matches the actual feedback received, it's a valid candidate
            if (computer.current_feedback['dead'] == temp_feedback_data['dead']
                and computer.current_feedback['injured'] == temp_feedback_data['injured']):
                new_possible_list.append(poss_pin)

        # Update the list of remaining possible pins
        computer.possible_pin_list = new_possible_list

# Testing/Mocking execution

player1 = PlayerModel('Donald')
player1.guess_count = 3
player2 = PlayerModel('joey')

player3 = PlayerModel('donald')
player3.guess_count = 7
player4 = PlayerModel('Joey')
file_name = '../D_n_I_leaderboard.json'
mock_logic = Logic()

mock_logic.save_to_leaderboard(file_name, winner=player1, loser=player2)
mock_logic.save_to_leaderboard(file_name, winner=player3, loser=player4)
print(mock_logic.get_sorted_leaderboard(file_name))
