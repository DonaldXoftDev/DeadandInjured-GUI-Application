from game_presenter import GamePresenter

names = ['donald', 'jake', 'michael']

#need a way to iterate round the players in the list
rounds = 10

def get_next_player():
    for i in range(len(names)):
        next_turn = (i + 1) % len(names)
        


#loop ten times for the 3 players and  tell the user the current round and whose player's turn it is
current_index = 0
for round in range(rounds):
    next_turn = (current_index) % len(names)
    next_player = names[next_turn]
    current_index += 1
    if current_index == len(names):
        current_index = 0
    print(f"Round {round + 1}: It is {next_player}'s turn")



