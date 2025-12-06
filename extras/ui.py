import tkinter as tk
import ttkbootstrap as ttk

from frontend_model.name_label_frame import NameLabelFrame


# --- Placeholder Logic Functions (Required for script to run) ---
# NOTE: You MUST have your actual logic functions imported or defined here
def validate_pin_or_guess(input_string: str) -> list:
    # Minimal validation to prevent errors
    if len(input_string) == 4 and input_string.isdigit():
        return [int(n) for n in input_string]
    return []


# --- CONSTANTS ---
THEME_COLOR = '#075B5E'
# NOTE: Use simple tuple for style configuration, NOT Font object
ENTRY_FONT_TUPLE = ('Arial', 20, 'bold')
INSTRUCTION = 'You have to enter 4 digit unique pin from 0 to 9'

class SetupUI:
    def __init__(self, master):
        self.master = master

        # NOTE: StringVar() must be imported as tk.StringVar if not using 'from tkinter import *'
        self.name_var = tk.StringVar()
        self.entry_boxes = []
        self.player_name = ''

        # --- Styles Setup ---
        style = ttk.Style()

        # 1. FIX: Define entry_font as a tuple for style configuration (size 20 is adequate)
        self.label_font = ('Arial', 20)

        # FIX: The entry font is now a tuple
        self.entry_font = ENTRY_FONT_TUPLE

        # Label style
        style.configure('TLabel', font=self.label_font, foreground='white')
        style.configure('name.TLabel', font=('Arial', 12), foreground='white')

        # FIX: Correctly configure TEntry with the tuple font
        style.configure('TEntry', font=self.entry_font, background=THEME_COLOR)

        # FIX: Using map is the most reliable way to force the font size
        style.map('Padded.TEntry', font=[('focus', self.entry_font)])
        style.configure('Padded.TEntry', padding=10, font=self.entry_font)

        # Button style
        style.configure('TButton', font=('Arial', 18), foreground='black')

        # Frame style
        style.configure('TFrame', background=THEME_COLOR)

        # --- UI Initialization ---
        self.window_frame = self.create_main_container()
        self.setup_frame = self.create_setup_screen()
        self.game_frame = self.create_game_screen()
        self.result_frame = self.create_result_screen()

        # FIX: Place the main container frame
        self.window_frame.grid(row=0, column=0, sticky='nsew')

        # Initial screen to display
        # FIX: Show setup_frame inside the window_frame
        self.setup_frame.grid(row=0, column=0, sticky='nsew')

        # Make the central grid cell of the root window expandable
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

    def create_main_container(self):
        # Anchor for all other frames (needed for padding/alignment)
        frame = ttk.Frame(self.master, style='TFrame', padding=100)
        return frame

    def create_setup_screen(self):
        frame = ttk.Frame(self.window_frame, style='TFrame',)

        # FIX: Add a container frame for the input area to centralize widgets
        input_container = ttk.Frame(frame, style='TFrame')
        # Place the container centrally
        input_container.grid(row=0, column=0, padx=10, pady=10)

        # Center the widgets within the container using column weight
        input_container.grid_columnconfigure(0, weight=1)

        # Label is inside the container
        title_label = ttk.Label(input_container, text="SETUP SCREEN",  bootstyle='success')
        title_label.grid(row=0, column=0, padx=10, pady=20)

        name_label = ttk.Label(input_container, text="Enter Your Name", )
        name_label.grid(row=1, column=0, padx=50, pady=10)

        name_entry = ttk.Entry(input_container, textvariable=self.name_var, width=10, style='Padded.TEntry')
        name_entry.grid(row=2, column=0, padx=10, pady=10)
        name_entry.focus()

        # Submit button is inside the container
        submit_name_btn = ttk.Button(input_container, text='SUBMIT', command=self.store_player_name,)
        submit_name_btn.grid(row=3, column=0, padx=10, pady=35)

        # Center the setup_frame within its parent cell (window_frame's grid)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        return frame

    def create_game_screen(self):
        frame = ttk.Frame(self.window_frame, style='TFrame')

        title_label = ttk.Label(frame, text="GAME SCREEN", style='TLabel')
        # Place title centrally, spanning the 4 entry columns
        title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

        # FIX: Clear the entry_boxes list before creating new ones (safety)
        self.entry_boxes.clear()

        # #entry frame
        # entry_frame = ttk.Frame(frame, style='TFrame')
        # entry_frame.grid(row=2, column=1, padx=100, pady=10)


        # FIX: The entry boxes need to be children of THIS frame
        instruction_label = ttk.Label(frame,style='TLabel', text=INSTRUCTION)
        instruction_label.grid(row=1, column=0, columnspan=4, padx=10, pady=20)

        sample_label_frame = ttk.LabelFrame(frame, text='Sample Data'.upper(),labelanchor='n', bootstyle='danger')
        sample_label_frame.grid(row=2, column=0, padx=10, pady=10)

        for i in range(4):
            # FIX: box_var is a local variable, not saved to self, but that's okay here
            box_var = tk.StringVar()

            # FIX: Added 'frame' as the parent
            box_entry = ttk.Entry(sample_label_frame, style='Padded.TEntry', textvariable=box_var, show='⚫', width=5)
            self.entry_boxes.append(box_entry)

      # FIX: Centering the Entry Boxes using grid and weight
        for i, box in enumerate(self.entry_boxes):
            box.grid(row=1, column=i, padx=10, pady=10)
            # FIX: Give equal weight to all 4 columns for centering
            frame.grid_columnconfigure(i, weight=1)

            # Submit button for the guess (placeholder)
        submit_input_btn = ttk.Button(sample_label_frame, text='GUESS',command=self.dummy_guess, style='TButton')

        submit_input_btn.grid(row=2, column=0, columnspan=4, pady=40)

        return frame

    def create_result_screen(self):
        frame = ttk.Frame(self.window_frame, style='TFrame')
        label = ttk.Label(frame, text="RESULT SCREEN", style='TLabel')
        label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        return frame

    def store_player_name(self):
        self.player_name = self.name_var.get()
        print(self.player_name.title())
        self.name_var.set('')

        # FIX: Correct transition call
        self.transition_to_new_screen(self.setup_frame, self.game_frame)

    def dummy_guess(self):
        print("Guess button clicked! Ready for game logic.")

    def transition_to_new_screen(self,old_frame, new_frame):
        # Hides the old frame
        old_frame.grid_forget()

        # Shows the new frame in the same cell
        new_frame.grid(row=0, column=0, sticky='nsew')


# # --- RUNNING THE APPLICATION ---
# # window = tkb.Window(themename='superhero')
# window = ttk.Window(themename='vapor')
# window.title('DEAD AND INJURED GAME')
# window.configure(background=THEME_COLOR)
# ui = SetupUI(window)
# window.mainloop()

class Trial:
    def __init__(self,master):
        self.master = master
        self.name = 'Donald'
        self.opp_name = 'computer'

        self.guess = ['1', '2', '9', '6']
        self.guess_vars = []

        self.guess_count = 20
        self.count_vars = []

        self.pin_vars = []

        self.result_frame = self.show_result_screen()


        self.result_frame.grid(row=0, column=0, sticky='nsew')

        #styles
        style = ttk.Style()

        style.configure('TLabel', font=('Helvetica', 15), )
        style.configure('TLabelframe.Label', font=('Helvetica', 12), )

        style.configure('TButton', font=('Helvetica', 12), padx=5, pady=5)

        style.configure('Pin.TEntry', font=('Helvetica', 12))
        style.configure('Count.TEntry', font=('Arial', 16), padding=[20,25])
        self.master.mainloop()

    def dummy_guess(self):
        print("Guess button clicked! Ready for game logic.")

    def toggle_switching(self,toggle_var):
        if toggle_var.get():
            for i, var in enumerate(self.pin_vars):
                var.set(self.guess[i])
        else:
            for i, var in enumerate(self.pin_vars):
                var.set('⚫')

    def show_result_screen(self):
        frame = ttk.Frame(self.master)

        main_frame = ttk.Frame(frame, style='TFrame')
        main_frame.grid(row=0,column=0,padx=12, pady=10)

        title_label = ttk.Label(main_frame,text="STATS",)
        title_label.grid(row=0, column=0, padx=(10, 300))

        horizontal_divider = ttk.Separator(main_frame, orient='horizontal')
        horizontal_divider.grid(row=1, column=0, columnspan=6,sticky='ew', padx=10, pady=10)

        # vertical_divider = ttk.Separator(main_frame, orient='vertical')
        # vertical_divider.grid(row=1, column=1, rowspan=10,sticky='ns', padx=(50,100), pady=10)

        main_frame.grid_columnconfigure(0, weight=1)
        for i in range(3):
            name_label_frame = NameLabelFrame(main_frame,self.name)
            name_label_frame.frame.grid(row=2, column=i, padx=10, pady=10)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        return frame

window = ttk.Window(themename='superhero')
trial = Trial(window)
