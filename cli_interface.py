

class Interface:
    def get_code_input(self, player_name: str, description) -> str:
        code = input(f'{player_name}, enter Your 4 unique digit {description} (0 - 9): ')
        return code


    def display_message(self, message: str) -> None:
        print(f'{message}\n')


    def display_error_message(self, message: str) -> None:
        print(f'ERROR: {message} \n')


    def get_player_name(self) -> str:
        entering_name = True
        new_player_name = None
        while entering_name:
            name = input('Enter your player name: ')
            if not name:
                print('Please enter a player name.')
                continue
            new_player_name = name
            entering_name = False
        return new_player_name


    def play_with_comp_prompt(self) -> str:
        response = input('Do you want to play again comp("y/n"): ').lower()
        return response

