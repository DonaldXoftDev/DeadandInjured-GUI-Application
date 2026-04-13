import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class TestLeaderboardApp:
    """
    A standalone test application to visualize and fine-tune the Leaderboard screen
    without running the entire game.
    """
    def __init__(self):
        # 1. Setup a dummy window with your app's theme
        self.window = ttk.Window(themename='superhero')
        self.window.title('Leaderboard Test')
        self.window.geometry('800x600')  # Give it a good default size

        # 2. Define the fonts your real GameView uses so it looks identical
        self.game_over_player_title_label = ('Inter', 32, 'bold')
        self.label_font = ('Arial', 20)

        style = ttk.Style()
        style.configure('success.Treeview', font=('Arial', 13), rowheight= 35)

        style.configure('Treeview.Heading', font=('Arial', 14, 'bold'))

        # 3. Create the frame
        self.leaderboard_frame = self.leaderboard_screen()
        
        # 4. Display the frame and make it expand to fill the window
        self.leaderboard_frame.grid(row=0, column=0, sticky='nsew')
        self.window.grid_columnconfigure(0, weight=1)

    # -------------------------------------------------------------------------
    # YOUR EXACT CODE (with minor parent/master fixes for Tkinter)
    # -------------------------------------------------------------------------
    def leaderboard_screen(self) -> ttk.Frame:
        frame = ttk.Frame(self.window,)

        comp_title_label = ttk.Label(
            frame,
            text='COMPUTER SCREEN',
            font=('Inter', 32, 'bold'),
            padding=(130,0)
        )
        comp_title_label.grid(row=0, column=1,columnspan=2, padx=10, pady=10)

        horiz_rule = ttk.Separator(orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        self.comp_inner_frame = ttk.Frame(frame)
        self.comp_inner_frame.grid(row=2, column=0, padx=10, pady=10)

        return frame

    def play_again_clicked(self):
        print("Play Again button clicked!")

    def start(self):
        self.window.mainloop()

# Run the test app
if __name__ == "__main__":
    app = TestLeaderboardApp()
    app.start()