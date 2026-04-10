from logging import raiseExceptions
from typing import Dict, Optional


class PlayerModel:
    """Represents a player in the Dead and Injured game, storing state and history."""

    def __init__(self,name: Optional[str] = None):
        """Initialize a new player with default game state."""
        self.name = name
        self.pin: list[int] = []
        self.guess: list[int] = []
        self.guess_count = 0
        self.current_feedback: dict[str, int] = {}
        self.feedback_history: list[str] = []
        self.is_human = True

    def set_name(self, name: str):
        """Set the player's display name."""
        self.name = name

    def get_name(self):
        """Return the player's name or an empty string if not set."""
        return self.name if self.name is not None else ''

    def update_pin(self,pin: list[int]):
        """Set the secret PIN for this player."""
        self.pin = pin

    def update_guess(self,guess: list[int]):
        """Update the player's most recent guess."""
        self.guess = guess

    def update_feed_back_history (self, feedback: str):
        """Append a feedback string to the player's history."""
        self.feedback_history.append(feedback)

    def update_current_feedback(self, data: dict[str, int]):
        """Update the current Dead and Injured counts."""
        self.current_feedback = data

    def increment_guess_count(self):
        """Increment the total number of guesses made."""
        self.guess_count += 1
