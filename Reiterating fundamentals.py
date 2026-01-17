# ==========================================
# 4. REAL-WORLD ARCHITECTURE CHALLENGE
# ==========================================
# Scenario: You have a list of guesses from your game.
# Some are correct (4 Dead), some are close, some are empty.

game_turns = [
    {"player": "Dami", "dead": 4, "injured": 0},
    {"player": "CPU-1", "dead": 1, "injured": 2},
    {"player": "Alice", "dead": 0, "injured": 0},
]

# TASK: Create a list of strings for the leaderboard.
# 1. Only include players who have at least ONE hit (Dead or Injured > 0).
# 2. Format: "NAME: [WINNER]" if dead == 4, else "NAME: [PLAYING]"
# Expected Result: ["Dami: [WINNER]", "CPU-1: [PLAYING]"]


leaderboard = [f'{p['player'].title()}: {'[WINNER]'if p['dead'] == 4 else '[PLAYING]'}'
                for p in game_turns if p['dead'] > 0 or p['injured'] > 0]
print(leaderboard)