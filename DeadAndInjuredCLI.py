from logic import (validate_pin_or_guess, compare_pin_to_guess,
                   computer_guessing_strategy, format_output, declare_winner,generate_feedback_table,
                   computer_generate_pin, format_list_to_string)
import random
import time
from itertools import  permutations

# ask user to select pin
def select_pin_or_guess(label="PIN"):
    pin_or_guess = input(f"Enter 4 digit unique {label.upper()}:").strip()
    valid_pin_or_guess = validate_pin_or_guess(pin_or_guess)
    return valid_pin_or_guess


def main():
    name = input("Enter your name: ").strip().lower()
    user_pin  = select_pin_or_guess()
    computer_pin = computer_generate_pin()


    if not user_pin:
        print('That is not a valid PIN.')
    else:
        possible_pins =  [list(pin) for pin in permutations(range(10), 4)]

        print('USER PIN:', format_list_to_string(user_pin))
        print('COMPUTER PIN:', format_list_to_string(computer_pin))

        computer_guess = computer_generate_pin()
        user_table_list  = []
        comp_table_list = []


        while True:
            print('\n')

            user_guess = select_pin_or_guess(label="Guess")

            print(computer_guess)
            if not user_guess:
                print('That is not a valid GUESS.')
                continue

            user_guess_to_string = format_list_to_string(user_guess)
            comp_guess_to_string = format_list_to_string(computer_guess)
            print('USER GUESS:',user_guess_to_string)
            print('\n**********COMPUTER IS GUESSING**********')
            time.sleep(1)
            print('COMPUTER GUESS:',comp_guess_to_string)

            user_result = compare_pin_to_guess(g_list=user_guess, p_list=computer_pin, name=name)

            if not user_result:
                print('No feedback received from computer.')
                continue

            comp_result = compare_pin_to_guess(g_list=computer_guess, p_list=user_pin, name='Computer')
            print(comp_result)


            print('\n----------CURRENT FEEDBACK-------')
            user_feedback_str = format_output(user_result)
            print(user_feedback_str)

            print('\n---------COMPUTER FEEDBACK--------')
            comp_feedback_str =format_output(comp_result)
            print(comp_feedback_str)


            user_table_list.append([user_guess_to_string, user_feedback_str])
            comp_table_list.append([comp_guess_to_string, comp_feedback_str])

            print('\n')
            print('=====FEEDBACK TABLES=======')
            user_table = generate_feedback_table(row_list=user_table_list , name=name)
            comp_table = generate_feedback_table(row_list=comp_table_list)
            print(user_table)
            print('\n')
            print(comp_table)

            new_pins = computer_guessing_strategy(previous_pins=possible_pins,
                                                       last_guess=computer_guess, last_result=comp_result
                                                       )
            # print(len(new_pins))

            if random.random() > 0.5:
                computer_guess = random.choice(new_pins)
            else:
                computer_guess = computer_generate_pin()

            possible_pins = new_pins


            result_data = [user_result, comp_result]
            results = declare_winner(results_list=result_data)

            if results['winner']:
                print('\n--------------WINNER-------------')
                print(f'The Winner is {results["name"].title()} 🤗🎉')
                print(f'computer pin : {computer_pin}\n user pin : {user_pin}')
                break



if '__main__' == __name__:
    main()
