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
        # The main container frame
        frame = ttk.Frame(self.window, padding=50)


        title_label = ttk.Label(frame, text='Leaderboard', font=self.game_over_player_title_label)
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10) # Centered across columns

        horiz_rule = ttk.Separator(frame, orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(5, 0))

        subtitle_text = 'Top 10 Dead and Injured Players Hall of Fame'
        subtitle_label = ttk.Label(frame, text=subtitle_text, font=self.label_font)
        subtitle_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        columns = ('rank', 'champion', 'loser', 'guesses')

        table = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            bootstyle='success',
            height=5, # Reduced slightly so buttons fit on screen better
        )

        table.heading('rank', text='Rank')
        table.heading('champion', text='Champion 🏆')
        table.heading('loser', text='Loser 💔')
        table.heading('guesses', text='Tries before Win')
        
        # BUG FIX 2: Widths in Treeview are in PIXELS, not characters. 
        # Width=10 pixels is microscopic. I've increased them so you can see the text.
        table.column('rank', width=2, anchor='center')
        table.column('champion', width=10, anchor='center')
        table.column('loser', width=10, anchor='center')
        table.column('guesses', width=10, anchor='center')
        
        table.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        
        # Scrollbar setup (Your logic here is perfect!)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        
        # Action Buttons Frame (Groups buttons together cleanly at the bottom)
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')
        
        exit_game_btn = ttk.Button(btn_frame, text='Exit', bootstyle='danger-outline')
        exit_game_btn.pack(side='left', padx=10)
        
        play_again_btn = ttk.Button(btn_frame, text='Play Again', bootstyle='success-outline', command=self.play_again_clicked)
        play_again_btn.pack(side='right', padx=10)
        
        # Allow the table row to expand if the window is resized
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1) 

        # --- DUMMY DATA INJECTION FOR TESTING ---
        # Let's add some fake data so you can actually see what the table looks like populated!
        dummy_data = [
            (1, 'Donald', 'Joey', 3),
            (2, 'Sarah', 'Mike', 4),
            (3, 'Alice', 'Bob', 5),
            (4, 'Charlie', 'Dave', 5),
            (5, 'Eve', 'Frank', 6),
            (6, 'Grace', 'Heidi', 7),
            (7, 'Ivan', 'Judy', 8),
            (8, 'Mallory', 'Oscar', 9),
            (9, 'Peggy', 'Sybil', 10),
            (10, 'Trent', 'Victor', 12),
            (11, 'Walter', 'Zoe', 15), # Extra row to test scrolling
        ]

        rank_dict = {1: '🏆', 2: '🥈', 3: '🥉'}

        current_rank = 0
        last_seen_score = None
        for record in dummy_data:
            guesses = record[3]

            if  guesses != last_seen_score:
                current_rank += 1
                rank = rank_dict.get(current_rank, current_rank)
            else:
                rank = rank_dict.get(current_rank, current_rank)

            last_seen_score = guesses

            champion_name = record[1]
            loser_name = record[2]

            table.insert('', 'end', values=(rank, champion_name, loser_name, guesses))

        return frame

    def play_again_clicked(self):
        print("Play Again button clicked!")

    def start(self):
        self.window.mainloop()

# Run the test app
if __name__ == "__main__":
    app = TestLeaderboardApp()
    app.start()