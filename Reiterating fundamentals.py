import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from dataclasses import dataclass
from ttkbootstrap.icons import Emoji

# --- DUMMY DATA STRUCTURES ---
@dataclass
class GameOverDetails:
    """Simulates the 'Baton' passed from the Logic/Presenter."""
    player_name: str
    player_guess_count: int
    time_spent: str = "0:45s"


class MockPresenter:
    """Simulates the Presenter to handle button clicks."""

    def restart_game_sequence(self):
        print("[MOCK] Restarting Game...")

    def view_rankings_sequence(self):
        print("[MOCK] Opening Leaderboard...")


# --- THE PROTOTYPE CLASS ---
class GameOverPrototype:
    def __init__(self):
        # Initialize the window with the 'superhero' theme from your project
        self.window = ttk.Window(themename='superhero')
        self.window.title("Dead & Injured - Game Over Vision")
        self.window.geometry("500x700")

        # Mock Presenter
        self.presenter = MockPresenter()

        # Build the screen
        self.main_frame = self.game_over_screen()
        self.main_frame.pack(expand=True, fill='both')

        # Simulate an update with dummy data
        test_data = GameOverDetails(
            player_name="Donald",
            player_guess_count=12,
            time_spent="1:15s"
        )


        loser_data = GameOverDetails(
            player_name= 'jonathan',
            player_guess_count= 11,
            time_spent= "2:45s"

        )
        self.update_game_over_content([test_data, loser_data])

    def game_over_screen(self) -> ttk.Frame:
        """
        A professional Game Over screen using a 'Card' layout.
        """
        # Main container with heavy padding to center everything
        frame = ttk.Frame(self.window, padding=(50, 80))

        # --- 1. THE HERO SECTION ---
        # Trophy Emoji (No assets needed!)
        trophy = Emoji.get('trophy')
        trophy_lbl = ttk.Label(frame, text=f'{trophy}', font=("Segoe UI Emoji", 60))
        trophy_lbl.pack(pady=(0, 10))



        self.win_header = ttk.Label(
            frame,
            text="CHAMPION!",
            font=('Inter', 32, 'bold'),
            bootstyle="success"
        )
        self.win_header.pack()

        self.winner_name_lbl = ttk.Label(
            frame,
            text="PLAYER 1",
            font=('Inter', 18),
            foreground="#adb5bd"  # Muted grey
        )
        self.winner_name_lbl.pack(pady=(0, 30))


        # --- 2. THE STATS CARD ---
        # A frame with a different background or border to act as a 'card'
        self.winner_stats_card = ttk.Labelframe(frame, text="Winner's Game Performance ", padding=20)
        self.winner_stats_card.pack(fill='x', padx=20, pady=20)

        self.loser_stats_card = ttk.Labelframe(frame, text="Loser's Game Performance ", padding=20)
        self.loser_stats_card.pack(fill='x', padx=20, pady=20)

        # We use a sub-grid for the stats to keep them aligned
        self.winner_stat = ttk.Label(self.winner_stats_card, text="Total Guesses: 0", font=('Inter', 12))
        self.winner_stat.grid(row=0, column=0, padx=20, sticky='w')

        self.winner_timer_stat = ttk.Label(self.winner_stats_card, text="Time Spent: 0:45s", font=('Inter', 12))
        self.winner_timer_stat.grid(row=0, column=1, padx=20, sticky='e')

        loser_emoji = ttk.Label(frame, text='❌', font=('Arial', 60))
        loser_emoji.pack(pady=(0, 10))

        self.loser_header = ttk.Label(
            frame,
            text="You Are A Loser!",
            font=('Inter', 32, 'bold'),
            bootstyle="danger"
        )
        self.loser_header.pack()
        self.loser_name_lbl = ttk.Label(
            frame,
            text="PLAYER 2",
            font=('Inter', 18),
            foreground='#adb5bd'
        )
        self.loser_name_lbl.pack(pady=(0, 30))

        self.loser_stat = ttk.Label(self.loser_stats_card, text="Total Guesses: 0", font=('Inter', 12))
        self.loser_stat.grid(row=1, column=0, padx=20, sticky='w')

        self.loser_timer_stat = ttk.Label(self.loser_stats_card, text="Time Spent: 0:45s", font=('Inter', 12))
        self.loser_timer_stat.grid(row=1, column=1, padx=20, sticky='e')

        # --- 3. THE ACTION ROW ---
        btn_container = ttk.Frame(frame)
        btn_container.pack(pady=40)

        # Primary Action (Play Again)
        ttk.Button(
            btn_container,
            text="PLAY AGAIN",
            bootstyle="success-outline",
            width=15,
            command=self.presenter.restart_game_sequence
        ).pack(side='left', padx=10)

        # Secondary Action (Leaderboard)
        ttk.Button(
            btn_container,
            text="LEADERBOARD",
            bootstyle="info-outline",
            width=15,
            command=self.presenter.view_rankings_sequence
        ).pack(side='left', padx=10)

        # Danger/Exit Action
        ttk.Button(
            btn_container,
            text="EXIT",
            bootstyle="danger-link",
            command=self.window.destroy
        ).pack(side='left', padx=10)

        return frame

    def update_game_over_content(self, data: list[GameOverDetails]):
        """
        Maps the 'Baton' (Data) to the visual elements.
        """
        self.winner_name_lbl.config(text=f"{data[0].player_name.upper()}")
        self.winner_stat.config(text=f"Total Guesses: {data[0].player_guess_count}")
        self.winner_timer_stat.config(text=f"Time Spent: {data[0].time_spent}")

        self.loser_name_lbl.config(text=f"{data[1].player_name.upper()}")
        self.loser_stat.config(text=f"Total Guesses: {data[1].player_guess_count}")
        self.loser_timer_stat.config(text=f"Time Spent: {data[1].time_spent}")

        # Contextual Styling: If CPU won, change color to Danger


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = GameOverPrototype()
    app.run()