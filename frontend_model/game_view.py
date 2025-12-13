import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from typing import Protocol, List, Optional

from game_presenter import RequiredDetails
from name_label_frame import NameLabel


class PresenterProtocol(Protocol):

    def create_players(self, state):
        ...

    def store_player_name(self, name: str):
        ...

    def store_player_code(self, pin: str):
        ...


    def update_stats(self):
        ...


class GameView:
    def __init__(self, presenter: Optional[PresenterProtocol]=None):
        self.window = ttk.Window(themename='superhero')
        self.window.grid(baseWidth=10, baseHeight=10, widthInc=10, heightInc=10)

        self.presenter = presenter

        # style
        style = ttk.Style()
        self.label_font = ('Arial', 20)
        self.button_font = ('Arial', 15)

        self.entry_vars = []
        self.entry_boxes = []

        # #frame style
        # style.configure('TFrame',)

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 15), )

        style.configure('TButton', font=('Helvetica', 12), padding=[40, 10])

        style.configure('TLabelframe.Label', font=('Helvetica', 12), )

        style.configure('Pin.TEntry', font=('Helvetica', 12))
        style.configure('Count.TEntry', font=('Arial', 16), padding=10)

        # label style
        style.configure('TLabel', font=self.label_font)
        style.configure('name.TLabel', font=('Helvetica', 15))
        style.configure('name.TLabelFrame.Label', font=('Helvetica', 15))

        self.home_frame = self.home_screen()
        self.setup_frame = self.setup_screen()
        self.pin_frame = self.pin_input_screen(player_name='Donald')
        self.guess_frame = self.guess_input_screen(player_name='Daniel')
        # self.comp_frame = self.comp_screen()
        stats_list = [RequiredDetails('phoebe',None,None),
                      RequiredDetails('jonathan',None,None)]

        self.stats_frame = self.stats_screen(stats_list)
        # self.game_over_frame = self.game_over_screen()


        # self.home_frame.grid(row=0, column=0, sticky='nsew')
        # self.setup_frame.grid(row=0, column=1, sticky='nsew')
        self.pin_frame.grid(row=0, column=0, sticky='nsew')
        # self.guess_frame.grid(row=0, column=0, sticky='nsew')
        # self.stats_frame.grid(row=0, column=0, sticky='nsew')


    def home_screen(self) -> ttk.Frame:
        frame = ttk.Frame(self.window, padding=40)

        title_frame = ttk.Frame(frame)
        title_frame.grid(row=0, column=0, sticky='nsew')
        title_frame.grid_columnconfigure(0, weight=1)

        dead_title_label = ttk.Label(title_frame, text="Dead")
        dead_title_label.grid(row=0, column=0)
        rule_1 = ttk.Separator(title_frame, orient='horizontal')
        rule_1.grid(row=0, column=1, columnspan=4, sticky='ew', )

        and_title_label = ttk.Label(title_frame, text="And")
        and_title_label.grid(row=1, column=1)
        rule_2 = ttk.Separator(title_frame, orient='horizontal')
        rule_2.grid(row=1, column=2, columnspan=2, sticky='ew', )

        injured_title_label = ttk.Label(title_frame, text="Injured")
        injured_title_label.grid(row=2, column=2)
        rule_3 = ttk.Separator(title_frame, orient='horizontal')
        rule_3.grid(row=2, column=3, columnspan=1, sticky='ew', )

        var = tk.StringVar()
        drop_menu = ttk.Menu(title_frame, tearoff=False)
        drop_menu.add_radiobutton(label='Player Vs Computer', variable=var, value='H_Vs_C')
        drop_menu.add_radiobutton(label='Player Vs Player', variable=var, value='H_Vs_H')

        menu_button = ttk.Menubutton(title_frame, text='Player Mode', bootstyle='info', menu= drop_menu)
        menu_button.grid(row=3, column=3, columnspan=1, pady=20)


        play_btn = ttk.Button(frame, text='PLAY GAME', bootstyle='success', command=None)

        play_btn.configure(padding=[95, 10], state=tk.DISABLED)
        play_btn.grid(row=1, column=0, pady=30)

        trace_back = lambda *args, mode_var=var, btn=play_btn: self.enable_btn(mode_var, btn)
        var.trace_add('write', trace_back)

        return frame

    def enable_btn(self, mode_var: tk.StringVar, btn: ttk.Button) -> None:
        if mode_var.get():
            btn.configure(state='enabled')
            # self.controller.create_players(mode_var.get())


    def setup_screen(self) -> ttk.Frame:
        frame = ttk.Frame(self.window, style='TFrame', padding=100)

        outer_setup_container = ttk.Frame(frame, style='TFrame')
        outer_setup_container.grid(row=0, column=0, sticky='nsew')

        # center the input frame on the parent frame
        outer_setup_container.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(outer_setup_container, text="SETUP SCREEN", style='TLabel')
        title_label.grid(row=0, column=1, padx=60, pady=10)

        horiz_rule = ttk.Separator(outer_setup_container, orient='horizontal')
        horiz_rule.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=(10, 50))

        prompt_label_frame = ttk.LabelFrame(outer_setup_container, text='ENTER A PLAYER NAME', labelanchor='n')
        prompt_label_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        input_frame = ttk.Frame(prompt_label_frame, style='TFrame')
        input_frame.grid(row=0, column=0, sticky='nsew', padx=70, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        var = tk.StringVar()
        name_entry = ttk.Entry(input_frame, textvariable=var, width=10, style='TEntry')
        name_entry.grid(row=0, column=1, padx=10, pady=30)
        name_entry.focus_set()

        submit_name_btn = ttk.Button(input_frame, text="SUBMIT", bootstyle='danger',command= None, padding=[40, 10])

        submit_name_btn.grid(row=1, column=1, padx=10, pady=10)

        frame.grid_columnconfigure(0, weight=1)
        # frame.bind('<Enter>', self.store_player_name)

        return frame

    def limit_length_to_1(self,var_to_check: tk.StringVar) -> None:
        if len(var_to_check.get().strip()) > 1:
            var_to_check.set(var_to_check.get().strip()[:1])

        elif len(var_to_check.get().strip()) == 0:
            var_to_check.set(var_to_check.get().strip())



    def jump_to_new_entry(self,event) -> None:
        index = self.entry_boxes.index(event.widget)
        current_var = self.entry_vars[index]
        next_index = index + 1

        if next_index < len(self.entry_boxes) and len(current_var.get()) > 0:
            self.entry_boxes[next_index].focus()


    def reverse_jump(self,event) -> None:
        index = self.entry_boxes.index(event.widget)
        current_var = self.entry_vars[index]
        previous_index = index - 1

        if previous_index >= 0 and not current_var.get():
            self.entry_boxes[previous_index].focus()

    def code_input_screen(self, player_name: str, label: str ='BaseCodeLabel') -> ttk.Frame:
        frame = ttk.Frame(self.window, style='TFrame', padding=50)

        title_label = ttk.Label(frame, text=f'WELCOME, {player_name} 🤗', style='TLabel')
        title_label.grid(row=0, column=0, columnspan=3, padx=(10, 200), pady=10)

        title_rule = ttk.Separator(frame, orient='horizontal')
        title_rule.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10, pady=(10, 50))

        instruction_label_frame = ttk.LabelFrame(frame, text=f'Enter 4 digit unique {label} from 0 to 9',
                                                 style='name.TLabelFrame', labelanchor='n')
        instruction_label_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        instruction_label_frame.grid_columnconfigure(0, weight=1)

        entry_frame = ttk.Frame(instruction_label_frame, style='TFrame', )
        entry_frame.grid(row=0, column=0, padx=50, pady=10, sticky='nsew')

        entry_frame.grid_columnconfigure(0, weight=1)
        # entry_frame.grid_columnconfigure(0, weight=1)  # Left Anchor Column
        # entry_frame.grid_columnconfigure(5, weight=1)


        self.entry_boxes.clear()
        self.entry_vars.clear()

        for i in range(4):
            box_var = tk.StringVar()
            box_entry = ttk.Entry(entry_frame, textvariable=box_var, style='TEntry', width=5, show='⚫')

            self.entry_vars.append(box_var)
            self.entry_boxes.append(box_entry)

            tracecallback = lambda *args, var_to_check=box_var: self.limit_length_to_1(box_var)

            # limits the size of input or  prevents entering space key
            if tracecallback:
                box_var.trace_add('write', tracecallback)
                box_entry.bind('<KeyRelease>', self.jump_to_new_entry)
                box_var.trace_add('unset', tracecallback)
                box_entry.bind('<KeyRelease-BackSpace>', self.reverse_jump)

            box_entry.grid(column=i, row=0, padx=10, pady=10)
            entry_frame.grid_columnconfigure(i, weight=1)

        submit_digits_btn = ttk.Button(entry_frame, text=f"CONFIRM {label.upper()}", bootstyle=SUCCESS,
                                       command=None, padding=[50, 10])
        submit_digits_btn.grid(row=1, column=0, columnspan=4, sticky='ew', padx=100, pady=40)

        return frame

    def pin_input_screen(self, player_name: str, label='PIN'):
        return self.code_input_screen(player_name, label)

    def guess_input_screen(self, player_name: str, label='GUESS'):
        return self.code_input_screen(player_name, label)

    def comp_screen(self):
        ...

    def stats_screen(self, required_stats: List[RequiredDetails]) -> ttk.Frame:

        frame = ttk.Frame(self.window, style='TFrame')

        main_frame = ttk.Frame(frame, style='TFrame')
        main_frame.grid(row=0, column=0, padx=10)

        title_label = ttk.Label(main_frame, text="STATS", )
        title_label.grid(row=0, column=0, padx=(10, 300))

        horizontal_divider = ttk.Separator(main_frame, orient='horizontal')
        horizontal_divider.grid(row=1, column=0, columnspan=6, sticky='ew', padx=10, pady=10)

        main_frame.grid_columnconfigure(1, weight=1)
        l_frames = []
        for i in range(len(required_stats)):
            name_label_frame = NameLabel(main_frame, required_stats[i])
            l_frames.append(name_label_frame)

        # labels.pop(0)
        if len(l_frames) > 1:
            for i,label in enumerate(l_frames):
                label.frame.grid(row=2, column=i, padx=10, pady=10)
                label.frame.grid_columnconfigure(i, weight=1)
        else:
            l_frames[0].frame.grid(row=2, column=0, padx=10, pady=10)

        guess_again_btn = ttk.Button(frame, text='GUESS AGAIN', bootstyle='success',
                                     command=None)

        guess_again_btn.grid(row=3, column=0, padx=50, pady=10)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        return frame

    def game_over_screen(self):
        ...


view = GameView()
view.window.mainloop()

