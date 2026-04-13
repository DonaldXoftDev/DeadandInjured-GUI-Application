import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from typing import Protocol, Any
from tkinter.messagebox import showwarning
from backend_models.game_data_model import  MainGameModel
from backend_models.game_screen_model import GameScreen
from backend_models.gameover_data_model import GameOverDetails
from backend_models.view_model import AppViewModel
from backend_models.stats_model import StatDetails
from frontend_model.name_label_frame import NameLabel
from backend_models.code_input_model import CodeInputViewModel


class PresenterProtocol(Protocol):
    """
    Protocol defining the expected interface for the Presenter.
    The GameView delegates user interactions and events to these methods.
    """

    def create_player_sequence(self, mode: str):
        """Handles the sequence when a player selects a game mode (e.g., 'H_Vs_C')."""
        ...

    def store_name_sequence(self, name: str):
        """Handles storing the player's name submitted via the setup screen."""
        ...

    def pin_submitted_sequence(self, pin: str):
        """Handles the submission of a player's initial 4-digit PIN."""
        ...

    def guess_submitted_sequence(self, guess: str):
        """Handles the submission of a 4-digit guess during the game."""
        ...

    def guess_again_sequence(self):
        """Handles transitioning the game back to the guess input screen for another turn."""
        ...

    def leaderboard_sequence(self) :
        ...

    def reset_sequence(self):
        ...


class GameView:
    """
    The main Graphical User Interface (GUI) class for the Dead and Injured game.
    It utilizes ttkbootstrap to manage different application screens.
    """

    def __init__(self, model: MainGameModel, presenter: PresenterProtocol = None):
        # Initialize the main window with a ttkbootstrap theme
        self.new_name_label_frame = None
        self.window = ttk.Window(themename='superhero')
        self.window.title('DEAD INJURED GUI')
        self.window.grid(baseWidth=10, baseHeight=10, widthInc=10, heightInc=10)
        self.game_model = model
        self.presenter = presenter

        # Set up standard fonts used across the application
        style = ttk.Style()
        self.label_font = ('Arial', 20)
        self.button_font = ('Arial', 15)
        self.game_over_label_font = ('Inter', 32, 'bold')
        self.emoji_font = ("Segoe UI Emoji", 60)

        style = ttk.Style()
        
        # Configure global styles for different ttk widgets
        style.configure('TLabel', font=('Helvetica', 15))
        style.configure('TButton', font=('Helvetica', 12), padding=[40, 10])
        style.configure('TLabelframe.Label', font=('Helvetica', 12))
        style.configure('Pin.TEntry', font=('Helvetica', 13))
        style.configure('Count.TEntry', font=('Arial', 16), padding=10)

        # Custom Label styles
        style.configure('TLabel', font=self.label_font)
        style.configure('name.TLabel', font=('Helvetica', 15))
        style.configure('name.TLabelFrame.Label', font=('Helvetica', 15))

        #Custom Treeview styles
        style.configure('success.Treeview', font=('Arial', 13), rowheight=35)
        style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))

        # Initialize placeholder attributes for dynamic UI elements
        self.name_entry = None
        self.pin_title_label = None
        self.guess_title_label = None
        self.box_entry = None
        self.emoji_label = None
        self.game_over_player_title_label = None
        self.table = None
        self.subtitle_label = None

        self.stats_inner_frame = None
        self.prompt_label_frame = None
        self.ui_player_index  = 0

        self.winner_act_pin_label= ttk.Label()
        self.loser_act_pin_label = ttk.Label()
        self.loser_name_label = ttk.Label()
        self.winner_name_label = ttk.Label()
        self.metric_message_label = ttk.Label()

        # Game variables for tracking input content
        self.player_mode = None
        self.name_var = None
        self.name_enty = None
        self.pin_var = []
        self.pin_enty = []
        self.guess_var = []
        self.guess_enty = []

        # Pre-build all screens (frames) to easily swap between them later
        self.home_frame = self.home_screen()
        self.setup_frame = self.setup_screen()
        self.pin_frame = self.pin_input_screen()
        self.guess_frame = self.guess_input_screen()
        self.stats_frame = self.stats_screen()
        self.leaderboard_frame = self.leaderboard_screen()
        self.game_over_frame = self.game_over_screen()

        # self.comp_frame = self.comp_screen()



    def start(self):
        """Starts the application by displaying the home screen and running the main loop."""
        self.home_frame.grid(row=0, column=0, sticky='nsew')
        self.window.mainloop()

    def home_screen(self) -> ttk.Frame:
        """Builds and returns the initial Home Screen for mode selection."""
        frame = ttk.Frame(self.window, padding=40)

        # Title Frame containing the title parts and separators
        title_frame = ttk.Frame(frame)
        title_frame.grid(row=0, column=0, sticky='nsew')
        title_frame.grid_columnconfigure(0, weight=1)

        # Title layout: "Dead --- And --- Injured ---"
        dead_title_label = ttk.Label(title_frame, text="Dead")
        dead_title_label.grid(row=0, column=0)
        rule_1 = ttk.Separator(title_frame, orient='horizontal')
        rule_1.grid(row=0, column=1, columnspan=3, sticky='ew', )

        and_title_label = ttk.Label(title_frame, text="And")
        and_title_label.grid(row=1, column=1)
        rule_2 = ttk.Separator(title_frame, orient='horizontal')
        rule_2.grid(row=1, column=2, columnspan=2, sticky='ew')

        injured_title_label = ttk.Label(title_frame, text="Injured")
        injured_title_label.grid(row=2, column=2)
        rule_3 = ttk.Separator(title_frame, orient='horizontal')
        rule_3.grid(row=2, column=3, columnspan=1, sticky='ew', )

        # Dropdown menu to select the play mode
        mode_var = tk.StringVar()
        self.player_mode = mode_var
        drop_menu = ttk.Menu(title_frame, tearoff=False)
        drop_menu.add_radiobutton(label='Player Vs Computer', variable=mode_var, value='H_Vs_C')
        drop_menu.add_radiobutton(label='Player Vs Player', variable=mode_var, value='H_Vs_H')

        leaderboard_btn = ttk.Button(
            title_frame,
            text='Leaderboards',
            command=lambda : self.presenter.leaderboard_sequence if self.presenter else None,
            bootstyle='success-outline'
        )
        leaderboard_btn.grid(row=3, column=0 ,pady= 20,)

        menu_button = ttk.Menubutton(title_frame, text='Player Mode', bootstyle='info', menu= drop_menu)
        menu_button.grid(row=3, column=3, pady=20)

        # Play button (initially disabled until a mode is chosen)
        play_btn = ttk.Button(title_frame, text='PLAY GAME', bootstyle='success-outline', command=self.mode_selected)
        play_btn.configure(padding=[95, 10], state=tk.DISABLED)
        play_btn.grid(row=4, column=0, columnspan=5, pady=30)


        # Attach a trace to the mode_var to enable the play button once a mode is selected
        trace_back = lambda *args, mode_vr=mode_var, btn=play_btn: self.enable_btn(mode_var, btn)
        mode_var.trace_add('write', trace_back)

        return frame

    def leaderboard_screen(self) -> ttk.Frame:
        """
        Builds and returns the Leaderboard screen.

        This screen is designed to display a sorted list of the top game records,
        featuring a title, a subtitle, a Treeview widget for the tabular data,
        and navigation buttons at the bottom.
        """
        # The main container frame
        frame = ttk.Frame(self.window, padding=50)

        title_label = ttk.Label(frame, text='Leaderboard', font=self.game_over_label_font)
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Centered across columns

        horiz_rule = ttk.Separator(frame, orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(5, 0))

        subtitle_text = 'Top 10 Dead and Injured Players Hall of Fame'
        self.subtitle_label = ttk.Label(frame, text=subtitle_text, font=self.game_over_player_title_label)
        self.subtitle_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        columns = ('rank', 'champion', 'loser', 'guesses')

        self.table = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            bootstyle='success',
            height=5,  # Reduced slightly so buttons fit on screen better
        )

        self.table.heading('rank', text='Rank')
        self.table.heading('champion', text='Champion 🏆')
        self.table.heading('loser', text='Loser 💔')
        self.table.heading('guesses', text='Tries before Win')

        # BUG FIX 2: Widths in Treeview are in PIXELS, not characters.
        # Width=10 pixels is microscopic. I've increased them so you can see the text.

        self.table.column('rank', width=2, anchor='center')
        self.table.column('champion', width=10, anchor='center')
        self.table.column('loser', width=10, anchor='center')
        self.table.column('guesses', width=20, anchor='center')

        self.table.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        # Scrollbar setup (Your logic here is perfect!)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')

        # Action Buttons Frame (Groups buttons together cleanly at the bottom)
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')

        exit_game_btn = ttk.Button(
            btn_frame,
            text='Exit',
            bootstyle='danger-outline',
            command= self.window.destroy,
        )
        exit_game_btn.pack(side='left', padx=10)

        play_again_btn = ttk.Button(
            btn_frame, text='Play Again',
            bootstyle='success-outline',
            command=self.play_again_clicked
        )
        play_again_btn.pack(side='right', padx=10)

        # Allow the self.table row to expand if the window is resized
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        return frame

    def enable_btn(self, mode_vr: tk.StringVar, btn: ttk.Button) -> None:
        """Enables the given button if the mode variable has a value."""
        if mode_vr.get():
            btn.configure(state='enabled')
        else:
            btn.configure(state='disabled')



    def setup_screen(self) -> ttk.Frame:
        """Builds and returns the setup screen where players input their names."""
        frame = ttk.Frame(self.window, style='TFrame', padding=100)

        outer_setup_container = ttk.Frame(frame, style='TFrame')
        outer_setup_container.grid(row=0, column=0, sticky='nsew')

        # center the input frame on the parent frame
        outer_setup_container.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(outer_setup_container, text="SETUP SCREEN", style='TLabel')
        title_label.grid(row=0, column=1, padx=60, pady=10)

        # Horizontal separator line
        horiz_rule = ttk.Separator(outer_setup_container, orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=(10, 50))

        # Label frame that instructs which player is entering their name
        self.prompt_label_frame = ttk.LabelFrame(outer_setup_container, text=f'PLAYER{self.ui_player_index}, ENTER A PLAYER NAME', labelanchor='n')
        self.prompt_label_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        input_frame = ttk.Frame(self.prompt_label_frame, style='TFrame')
        input_frame.grid(row=0, column=0, sticky='nsew', padx=70, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        # The entry box for the player name
        name_var = tk.StringVar()
        self.name_var = name_var
        name_entry = ttk.Entry(input_frame, textvariable=name_var, width=10, style='TEntry')
        self.name_entry = name_entry

        name_entry.grid(row=0, column=1, padx=10, pady=30)

        # Submit button for the name input
        submit_name_btn = ttk.Button(input_frame, text="SUBMIT", bootstyle='danger-outline',command= self.name_entered, padding=[40, 10])
        submit_name_btn.grid(row=1, column=1, padx=10, pady=10)

        frame.grid_columnconfigure(0, weight=1)

        return frame

    def limit_length_to_1(self,targe_list: list , index: int) -> None:
        """Restricts an Entry box's content to a maximum of 1 character."""
        current_content = targe_list[index].get().strip()
        if len(current_content) > 1:
            targe_list[index].insert(tk.END, current_content[:1])


    def jump_to_nxt_entry(self, event, target_list: list, index: int) -> None:
        """
        Automatically shifts focus to the next entry box in the sequence 
        once the current one is filled.
        """
        current_content =target_list[index].get().strip()
        next_index = index + 1

        # makes sure the next box is available for jumping
        if next_index < len(target_list):
            if current_content:
                target_list[next_index].focus_set()

    def allow_only_numbers(self, target_list:list, index: int):
        """Clears the entry box if the inputted character is not a digit."""
        num_strings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        content = target_list[index].get().strip()
        if content not in num_strings:
            target_list[index].delete(0, tk.END)

    def reverse_jump(self, event, target_list: list , index: int) -> None:
        """
        Automatically shifts focus to the previous entry box when Backspace 
        is pressed on an empty entry box.
        """
        content = target_list[index].get().strip()
        previous_index = index - 1

        if len(content) == 0:
            if previous_index >= 0:
                target_list[previous_index].focus_set()

                target_list[previous_index].delete(0, tk.END)

                target_list[previous_index].icursor(0)

    def code_input_screen(self,code_vm: CodeInputViewModel) -> ttk.Frame:
        """Builds a generic 4-digit code input screen, used for both PIN and Guess inputs."""
        frame = ttk.Frame(self.window, style='TFrame', padding=50)

        # Set dynamic labels depending on whether it's a PIN or GUESS screen
        if code_vm.screen_type.lower() == 'pin':
            self.pin_title_label = ttk.Label(frame, text=f'INITIALISED PLAYER NAME', style='TLabel')
            self.pin_title_label.grid(row=0, column=0, columnspan=3, padx=(10, 200), pady=10)
        else:
            self.guess_title_label = ttk.Label(frame, text=f'INITIALISED PLAYER NAME', style='TLabel')
            self.guess_title_label.grid(row=0, column=0, columnspan=3, padx=(10, 200), pady=10)

        title_rule = ttk.Separator(frame, orient='horizontal')
        title_rule.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10, pady=(10, 50))

        instruction_label_frame = ttk.LabelFrame(frame, text=f'Enter 4 digit unique {code_vm.label} from 0 to 9',
                                                 style='name.TLabelFrame', labelanchor='n')
        instruction_label_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        instruction_label_frame.grid_columnconfigure(0, weight=1)

        entry_frame = ttk.Frame(instruction_label_frame, style='TFrame', )
        entry_frame.grid(row=0, column=0, padx=50, pady=10, sticky='nsew')

        entry_frame.grid_columnconfigure(0, weight=1)

        # Reference appropriate instance variables based on screen type
        target_entries = self.pin_enty if code_vm.screen_type.lower() == 'pin' else self.guess_enty
        target_vars = self.pin_var if code_vm.screen_type.lower() == 'pin' else self.guess_var

        for i in range(4):
            box_var = tk.StringVar()
            box_entry = ttk.Entry(entry_frame, textvariable=box_var, style='TEntry', width=5, show='⚫')

            target_entries.append(box_entry)
            target_vars.append(box_var)

            is_only_numbers = lambda *args, tl=target_entries, idx = i: self.allow_only_numbers(tl, idx)
            if is_only_numbers:
                # Validate numbers only upon variable update
                box_var.trace_add('write', is_only_numbers)
                limit_to_1 =  lambda *args, tl=target_entries, idx=i: self.limit_length_to_1(tl, idx)

                if limit_to_1:
                    # Enforce the 1 character limit
                    box_var.trace_add('write', limit_to_1)

                    # Bind the release of a valid key to jump to the next possible box
                    box_entry.bind('<KeyRelease>', lambda event, tl=target_entries, idx = i:
                    self.jump_to_nxt_entry(event, tl, idx))

                    # Bind the release of a backspace key to jump to the previous possible box
                    box_entry.bind('<KeyPress-BackSpace>', lambda event, tl= target_entries, idx = i:
                    self.reverse_jump(event, tl, idx))

            # Summarized logic goals for the entry box:
            # - Only numbers allowed.
            # - Only 1 digit per box.
            # - Auto-advance or auto-reverse cursor focus.

            box_entry.grid(column=i, row=0, padx=10, pady=10)
            entry_frame.grid_columnconfigure(i, weight=1)

        btn_color = 'success-outline' if code_vm.screen_type == 'pin' else 'danger-outline'
        submit_digits_btn = ttk.Button(entry_frame,
                                       text=f"CONFIRM {code_vm.label.upper()}",
                                       bootstyle= btn_color,
                                       command=code_vm.command_on_click,
                                       padding=[50, 10]
                                       )
        submit_digits_btn.grid(row=1, column=0, columnspan=4, sticky='ew', padx=100, pady=40)
        return frame

    def pin_input_screen(self, label='PIN'):
        """Constructs and returns the screen specifically configured for PIN input."""
        type: str = label.lower()
        p_command = self.pin_submitted
        pin_vm = CodeInputViewModel(screen_type=type, label=label, command_on_click=p_command)
        return self.code_input_screen(pin_vm)

    def guess_input_screen(self,label: str ='GUESS'):
        """Constructs and returns the screen specifically configured for GUESS input."""
        type: str = label.lower()
        g_command = self.guess_submitted
        guess_vm = CodeInputViewModel(screen_type=type, label=label, command_on_click=g_command)
        return self.code_input_screen(guess_vm)

    def stats_screen(self) -> ttk.Frame:
        """Builds and returns the Stats Screen displaying match metrics."""
        frame = ttk.Frame(self.window, style='TFrame')

        self.stats_inner_frame = ttk.Frame(frame, style='TFrame')
        self.stats_inner_frame.grid(row=0, column=0, padx=10)

        title_label = ttk.Label(self.stats_inner_frame, text="STATS", )
        title_label.grid(row=0, column=0, padx=(10, 300))

        horizontal_divider = ttk.Separator(self.stats_inner_frame, orient='horizontal')
        horizontal_divider.grid(row=1, column=0, columnspan=6, sticky='ew', padx=10, pady=10)

        self.stats_inner_frame.grid_columnconfigure(1, weight=1)

        guess_again_btn = ttk.Button(frame, text='GUESS AGAIN', bootstyle='success-outline',
                                     command=self.guess_again_clicked)

        guess_again_btn.grid(row=3, column=0, padx=50, pady=10)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        return frame

    def comp_screen(self):
        """Placeholder for the 'Computer thinking/loading' screen layout."""
        frame = ttk.Frame(self.window, )

        comp_title_label = ttk.Label(
            frame,
            text='COMPUTER SCREEN',
            font=('Inter', 32, 'bold'),
            padding=(130, 0)
        )
        comp_title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        horiz_rule = ttk.Separator(orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        self.comp_inner_frame = ttk.Frame(frame)
        self.comp_inner_frame.grid(row=2, column=0, padx=10, pady=10)

        return frame

    def game_over_screen(self):
        """Builds and returns the Game Over Screen to show final results."""
        frame = ttk.Frame(self.window, padding=(20, 40))

        game_over_title = ttk.Label(
            frame, text="GAME OVER",
            font=self.game_over_label_font,
            foreground= '#FF2929'
        )
        game_over_title.grid(row=0, column=0, padx=10)

        horiz_rule = ttk.Separator(
            frame,
            orient='horizontal',
        )
        horiz_rule.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        # Inner frame serving as the container for results and actions
        inner_frame = ttk.Frame(
            frame,
            style='TFrame'
        )
        inner_frame.grid(row=2, column=0, padx=10, sticky='nsew')

        # Frame for displaying the Winner and Loser details side-by-side
        player_outcome_frame = ttk.Frame(
            inner_frame,
            style='TFrame',
        )
        player_outcome_frame.grid(row=0, column=0, padx=10, sticky='nsew')

        winner_frame = self.player_result_frame(
            player_outcome_frame,
            emoji='🏆',
            title= 'Champion!',
            player_name= 'Winner!',
            is_winner=True
        )
        winner_frame.grid(row=0, column=0, padx=10, pady=10)

        loser_frame = self.player_result_frame(
            player_outcome_frame,
            emoji= '💔',
            title= 'Failure!',
            player_name= 'Loser!'
        )
        loser_frame.grid(row=0, column=2, padx=(180, 10), pady=10)

        metrics_frame = ttk.Frame(
            inner_frame,
            style='TFrame'
        )
        metrics_frame.grid(row=1, column=0, padx=10)

        game_metrics_lf = self.game_metrics_label_frame(metrics_frame)
        game_metrics_lf.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        btn_frame = self.game_over_btn_frame(inner_frame)
        btn_frame.grid(row=2, column=0, padx = 10, pady= (30, 0), sticky='nsew')

        btn_frame.grid_columnconfigure(1, weight=1)

        inner_frame.grid_columnconfigure(0, weight=1)

        return frame

    def game_over_btn_frame(self, master: ttk.Frame):
        """Constructs the navigation buttons displayed on the Game Over screen."""
        frame = ttk.Frame(
            master,
            style='TFrame'
        )

        leader_board_btn = ttk.Button(
            frame,
            text='LEADERBOARD',
            bootstyle = 'info-outline',
            command= lambda: self.presenter.leaderboard_sequence() if self.presenter else None
        )
        leader_board_btn.grid(row=0, column=0, padx=10, sticky='w')

        # FIX: The command was executed immediately because self.presenter 
        # was None during GameView initialization (__init__).
        # Use lambda: to defer execution until the button is clicked.
        play_again_btn = ttk.Button(
            frame,
            text='PLAY AGAIN',
            bootstyle = 'success-outline',
            command= lambda: self.play_again_clicked() if self.presenter else None
        )
        play_again_btn.grid(row=0, column=1, padx=10, sticky='n')

        exit_btn = ttk.Button(
            frame,
            text='Exit',
            bootstyle = 'danger-link',
            command= self.window.destroy
        )
        exit_btn.grid(row=0, column=2, padx=10, sticky='e')

        return frame

    def format_to_string(self, data: list[int]) -> str:
        """Formats a list of integers into a spaced string (e.g., [1,2] -> '1 2')."""
        return ' '.join(map(str, data))

    def game_metrics_label_frame(self, master: ttk.Frame):
        """Builds the frame containing the detailed metrics at the end of the game."""
        frame = ttk.LabelFrame(
            master,
            text= 'Game Performance Metrics',
            labelanchor= 'nw',
        )

        winner_pin_label = ttk.Label(
            frame,
            text= "Winner's Pin",
            font = self.label_font,
            foreground= '#adb5bd'
        )
        winner_pin_label.grid(row=0, column=0, padx=10, pady=(10,0))

        loser_pin_label = ttk.Label(
            frame,
            text= "Loser's Pin",
            font =  self.label_font,
            foreground= '#adb5bd'
        )
        loser_pin_label.grid(row=0, column=1, padx=(290, 10), pady=(10,0))


        self.winner_act_pin_label = ttk.Label(
            frame,
            text= ' '.join(n for n in '2057'),
            font =('Inter', 15, 'bold'),
            foreground= '#adb5bd'

        )
        self.winner_act_pin_label.grid(row=1, column=0, padx=(5,10), pady=5)

        self.loser_act_pin_label = ttk.Label(
            frame,
            text = ' '.join(n for n in '3091'),
            font= ('Inter', 15, 'bold'),
            foreground= '#adb5bd'
        )
        self.loser_act_pin_label.grid(row=1, column=1, padx=(290,5), pady=5)

        self.metric_message_label  = ttk.Label(
            frame,
            text= "Winner guessed Loser's Pin in 5 tries",
            font = self.label_font,
            foreground='#adb5bd'

        )

        self.metric_message_label.grid(row=2,columnspan=3, padx=10, pady=(2,10), sticky='nsew')

        return frame

    def player_result_frame(self, master: ttk.Frame, emoji: str, title: str, is_winner=False, player_name=None)-> ttk.Frame:
        """Builds a UI block displaying a player's outcome (winner or loser info)."""
        frame = ttk.Frame(master)
        self.emoji_label = ttk.Label(
            frame,
            text=emoji,
            font=self.emoji_font ,
            foreground= '#FFE100' if emoji == '🏆' else '#FF2929'
        )
        self.emoji_label.grid(row=0, column=0, padx=10, pady=10,)

        game_over_player_title_label =ttk.Label(
            frame,
            text=title,
            font=self.game_over_label_font,
            foreground = '#08CB00' if is_winner else '#FF2929'
        )
        game_over_player_title_label.grid(row=1, column=0, padx=10, pady=10)

        game_over_player_name_label = ttk.Label(
            frame,
            text=player_name,
            font=self.label_font,
            foreground='#adb5bd'
        )
        game_over_player_name_label.grid(row=2, column=0, padx=10, pady=10)

        if is_winner:
            self.winner_name_label  = game_over_player_name_label
        else:
            self.loser_name_label = game_over_player_name_label


        return frame

    def update_leaderboard_table(self, data: list[dict]):
        rank_dict = {1: '🏆', 2: '🥈', 3: '🥉'}

        new_subtitle_text = f'Top {len(data)} Dead and injured  Players Hall of Fame!'
        self.subtitle_label.configure(text=new_subtitle_text)

        till_max_top_10 = data[:10]

        current_rank = 0
        last_seen_score = None
        for record in till_max_top_10:
            guesses = record.get('winner_guess_count', 0)

            if guesses != last_seen_score:
                current_rank += 1
                rank = rank_dict.get(current_rank,current_rank)
            else:
                rank = rank_dict.get(current_rank, current_rank)

            last_seen_score = guesses

            champion_name = record.get('winner', 'Unknown')
            loser_name = record.get('loser', 'Unknown')


            self.table.insert('', 'end', values=(rank, champion_name, loser_name, guesses))


    # -----------------------------------------------------
    # Methods callable by the Presenter to control the View
    # -----------------------------------------------------

    def display_error_popup(self, label: str , message: str):
        """Displays a warning dialog to the user with the specified message."""
        showwarning(title=f'INVALID {label}', message=message)

    def render_new_screen(self, vm: AppViewModel):
        """
        Changes the currently displayed view based on the AppViewModel.
        It hides all frames and only unhides the active one.
        """
        # Hide all existing screens
        self.home_frame.grid_forget()
        self.setup_frame.grid_forget()
        self.guess_frame.grid_forget()
        self.pin_frame.grid_forget()
        self.stats_frame.grid_forget()
        self.game_over_frame.grid_forget()
        self.leaderboard_frame.grid_forget()

        if vm.screen == GameScreen.MODE_SELECT:
            self.home_frame.grid(row=0, column=0, sticky='nsew')

        elif vm.screen  == GameScreen.NAME_SETUP:
            self.update_name_setup_index()
            self.setup_frame.grid(row=0, column=0, sticky='nsew')
            self.window.update_idletasks()
            self.name_entry.focus_set()

        elif vm.screen == GameScreen.PIN_ENTRY:
            screen_type = 'pin'
            self.update_code_frame_content(vm.details.player_name, screen_type)
            self.pin_frame.grid(row=0, column=0, sticky='nsew')
            self.window.update_idletasks()

            if self.pin_enty:
                self.pin_enty[0].focus()

        elif vm.screen == GameScreen.GUESS_ENTRY:
            screen_type = 'guess'
            self.update_code_frame_content(vm.details.player_name, screen_type)
            self.guess_frame.grid(row=0, column=0, sticky='nsew')
            self.window.update_idletasks()

            if self.guess_enty:
                self.guess_frame.after(50, lambda: self.guess_enty[0].focus_set())

        elif vm.screen == GameScreen.STATS_SCREEN:
            self.update_stat_screen(vm.details.sub_stats)
            self.stats_frame.grid(row=0, column=0, sticky='nsew')

        elif vm.screen == GameScreen.GAME_OVER:
            self.update_game_over_screen(vm.details)
            self.game_over_frame.grid(row=0, column=0, sticky='nsew')

        elif vm.screen == GameScreen.LEADERBOARD:
            self.update_leaderboard_table(vm.details)
            self.leaderboard_frame.grid(row=0, column=0, sticky='nsew')


    def update_code_frame_content(self, player_name: str, screen_type: str):
        """Updates the header text in the PIN or GUESS screen to greet the current player."""
        if self.pin_title_label is None or self.guess_title_label is None:
            print('Error; The title frame is still None')

        new_text = f'WELCOME, {player_name.title()} 🤗'
        if screen_type.lower() == 'guess':
            self.guess_title_label.configure(text=new_text)
        else:
            self.pin_title_label.configure(text=new_text)

    def update_name_setup_index(self):
        """Updates the prompt index indicating which player is currently entering their name."""
        if self.prompt_label_frame is None:
            print('Error; The name frame is still None')

        else:
            self.ui_player_index += 1
            new_text = f'PLAYER{self.ui_player_index}, ENTER A PLAYER NAME'
            self.prompt_label_frame.configure(text=new_text)

    def update_game_over_screen(self, details: GameOverDetails):
        """Populates the Game Over screen using data provided in GameOverDetails."""
        self.winner_name_label.configure(text=details.winner_name.upper())
        self.loser_name_label.configure(text=details.loser_name.upper())

        winner_pin_string = self.format_to_string(details.winner_pin)
        self.winner_act_pin_label.configure(text=winner_pin_string)

        loser_pin_string = self.format_to_string(details.loser_pin)
        self.loser_act_pin_label.configure(text=loser_pin_string)

        new_text = (f"{details.winner_name.title()} guessed {details.loser_name.title()}'s pin in "
                    f"{details.winner_guess_count} tries")

        self.metric_message_label.configure(text=new_text)

    def update_stat_screen(self, sub_stats: list[StatDetails]):
        """Populates the Stats screen with ongoing or historical match details."""
        if self.stats_inner_frame is None:
            print('Error; The stat main frame is still None')

        l_frames = []
        for i in range(len(sub_stats)):
            self.new_name_label_frame = NameLabel(self.stats_inner_frame, sub_stats[i])
            l_frames.append(self.new_name_label_frame)

        if len(l_frames) > 1:
            for i, label in enumerate(l_frames):
                label.frame.grid(row=2, column=i, padx=10, pady=10)
                label.frame.grid_columnconfigure(i, weight=1)
        else:
            l_frames[0].frame.grid(row=2, column=0, padx=10, pady=10)

    # -----------------------------------------------------
    # Event handlers bounded to View actions/buttons
    # -----------------------------------------------------

    def mode_selected(self):
        """Triggered when 'PLAY GAME' is clicked; notifies Presenter of mode choice."""
        self.presenter.create_player_sequence(self.player_mode.get())

    def reset_ui_state(self):
        # 1. Reset the dropdown variable correctly using .set()
        if isinstance(self.player_mode, tk.StringVar):
            self.player_mode.set('')

        # 2. Reset the player index counter
        self.ui_player_index = 0

        # 3. Physically destroy old stat frames from the previous game
        if self.stats_inner_frame:
            for widget in self.stats_inner_frame.winfo_children():
                # We only want to destroy the player stat frames (which you put in row 2)
                # We don't want to destroy the "STATS" title or the separator!
                grid_info = widget.grid_info()
                if grid_info and grid_info.get('row') == 2:
                    widget.destroy()

        # 4. Clear out the old guess variables so they don't pop up again
        for entry_var in self.pin_var:
            entry_var.set('')
        for entry_var in self.guess_var:
            entry_var.set('')

        self.table.delete(*self.table.get_children())


    def name_entered(self):
        """Triggered when a name is submitted; reads the name and forwards to Presenter."""
        name = self.name_var.get()
        self.name_entry.delete(0, tk.END)
        self.presenter.store_name_sequence(name)

    def pin_submitted(self):
        """Assembles the PIN from the 4 input boxes, notifies Presenter, and clears inputs."""
        pin_string = ''.join(p.get() for p in self.pin_enty if p.get())
        self.presenter.pin_submitted_sequence(pin_string)

        for p in self.pin_enty:
            p.delete(0, tk.END)

        if self.pin_enty: self.pin_enty[0].focus_set()

    def guess_submitted(self):
        """Assembles the Guess from the 4 input boxes, notifies Presenter, and clears inputs."""
        guess_string = ''.join(g.get() for g in self.guess_enty if g.get())
        self.presenter.guess_submitted_sequence(guess_string)

        for g in self.guess_enty:
            g.delete(0, tk.END)

        if self.guess_enty: self.guess_enty[0].focus_set()

    def guess_again_clicked(self):
        """Triggered when 'GUESS AGAIN' is clicked on the stats screen."""
        self.presenter.guess_again_sequence()

    def play_again_clicked(self):
        self.presenter.reset_sequence()


# Code for isolated UI testing:
# model = MainGameModel()
# view = GameView(model=model)
# view.start()