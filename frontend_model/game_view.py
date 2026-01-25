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

    def create_player_sequence(self, mode: str):
        ...

    def store_name_sequence(self, name: str):
        ...

    def pin_submitted_sequence(self, pin: str):
        ...

    def guess_submitted_sequence(self, guess: str):
        ...

    def guess_again_sequence(self):
        ...



class GameView:

    def __init__(self, model: MainGameModel, presenter: PresenterProtocol = None):


        self.window = ttk.Window(themename='superhero')
        self.window.title('DEAD INJURED GUI')
        self.window.grid(baseWidth=10, baseHeight=10, widthInc=10, heightInc=10)
        self.game_model = model
        self.presenter = presenter


        # style
        style = ttk.Style()
        self.label_font = ('Arial', 20)
        self.button_font = ('Arial', 15)
        self.game_over_label_font = ('Inter', 32, 'bold')
        self.emoji_font = ("Segoe UI Emoji", 60)

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 15), )

        style.configure('TButton', font=('Helvetica', 12), padding=[40, 10])

        style.configure('TLabelframe.Label', font=('Helvetica', 12), )

        style.configure('Pin.TEntry', font=('Helvetica', 13))
        style.configure('Count.TEntry', font=('Arial', 16), padding=10)

        # label style
        style.configure('TLabel', font=self.label_font)
        style.configure('name.TLabel', font=('Helvetica', 15))
        style.configure('name.TLabelFrame.Label', font=('Helvetica', 15))

        self.name_entry = None
        self.pin_title_label = None
        self.guess_title_label = None
        self.box_entry = None
        self.emoji_label = None
        self.game_over_player_title_label = None

        self.stats_inner_frame = None
        self.prompt_label_frame = None
        self.ui_player_index  = 0

        self.winner_act_pin_label= ttk.Label()
        self.loser_act_pin_label = ttk.Label()
        self.loser_name_label = ttk.Label()
        self.winner_name_label = ttk.Label()
        self.metric_message_label = ttk.Label()

        #all game_vars for simulating the screen transition
        self.player_mode = None
        self.name_var = None
        self.name_enty = None
        self.pin_var = []
        self.pin_enty = []
        self.guess_var = []
        self.guess_enty = []


        self.home_frame = self.home_screen()
        self.setup_frame = self.setup_screen()
        self.pin_frame = self.pin_input_screen()
        self.guess_frame = self.guess_input_screen()
        self.stats_frame = self.stats_screen()
        self.game_over_frame = self.game_over_screen()
        # self.comp_frame = self.comp_screen()



    def start(self):
        self.home_frame.grid(row=0, column=0, sticky='nsew')
        self.window.mainloop()

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

        mode_var = tk.StringVar()
        self.player_mode = mode_var
        drop_menu = ttk.Menu(title_frame, tearoff=False)
        drop_menu.add_radiobutton(label='Player Vs Computer', variable=mode_var, value='H_Vs_C')
        drop_menu.add_radiobutton(label='Player Vs Player', variable=mode_var, value='H_Vs_H')

        menu_button = ttk.Menubutton(title_frame, text='Player Mode', bootstyle='info', menu= drop_menu)
        menu_button.grid(row=3, column=3, columnspan=1, pady=20)


        play_btn = ttk.Button(frame, text='PLAY GAME', bootstyle='success-outline', command=self.mode_selected)

        play_btn.configure(padding=[95, 10], state=tk.DISABLED)
        play_btn.grid(row=1, column=0, pady=30)

        trace_back = lambda *args, mode_vr=mode_var, btn=play_btn: self.enable_btn(mode_var, btn)
        mode_var.trace_add('write', trace_back)

        return frame

    def enable_btn(self, mode_vr: tk.StringVar, btn: ttk.Button) -> None:
        if mode_vr.get():
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

        self.prompt_label_frame = ttk.LabelFrame(outer_setup_container, text=f'PLAYER{self.ui_player_index}, ENTER A PLAYER NAME', labelanchor='n')
        self.prompt_label_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        input_frame = ttk.Frame(self.prompt_label_frame, style='TFrame')
        input_frame.grid(row=0, column=0, sticky='nsew', padx=70, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        name_var = tk.StringVar()
        self.name_var = name_var
        name_entry = ttk.Entry(input_frame, textvariable=name_var, width=10, style='TEntry')
        self.name_entry = name_entry

        name_entry.grid(row=0, column=1, padx=10, pady=30)


        submit_name_btn = ttk.Button(input_frame, text="SUBMIT", bootstyle='danger-outline',command= self.name_entered, padding=[40, 10])

        submit_name_btn.grid(row=1, column=1, padx=10, pady=10)

        frame.grid_columnconfigure(0, weight=1)

        return frame

    def limit_length_to_1(self,targe_list: list , index: int) -> None:
        current_content = targe_list[index].get().strip()
        if len(current_content) > 1:
            targe_list[index].insert(tk.END, current_content[:1])


    def jump_to_nxt_entry(self, event, target_list: list, index: int) -> None:
        current_content =target_list[index].get().strip()
        next_index = index + 1

        #makes sure the next box is available for jumping
        if next_index < len(target_list):
            if current_content:
                target_list[next_index].focus_set()

    def allow_only_numbers(self, target_list:list, index: int):
        num_strings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        content = target_list[index].get().strip()

        if content not in num_strings:
            target_list[index].delete(0, tk.END)

    def reverse_jump(self, event, target_list: list , index: int) -> None:
        content = target_list[index].get().strip()
        previous_index = index - 1

        if len(content) == 0:
            if previous_index >= 0:
                target_list[previous_index].focus_set()

                target_list[previous_index].delete(0, tk.END)

                target_list[previous_index].icursor(0)

    def code_input_screen(self,code_vm: CodeInputViewModel) -> ttk.Frame:
        frame = ttk.Frame(self.window, style='TFrame', padding=50)

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

        target_entries = self.pin_enty if code_vm.screen_type.lower() == 'pin' else self.guess_enty
        target_vars = self.pin_var if code_vm.screen_type.lower() == 'pin' else self.guess_var

        for i in range(4):
            box_var = tk.StringVar()
            box_entry = ttk.Entry(entry_frame, textvariable=box_var, style='TEntry', width=5, show='⚫')

            target_entries.append(box_entry)
            target_vars.append(box_var)

            is_only_numbers = lambda *args, tl=target_entries, idx = i: self.allow_only_numbers(tl, idx)
            if is_only_numbers:
                # tracks when a number is written inside the box variable so to check if is
                box_var.trace_add('write', is_only_numbers)
                limit_to_1 =  lambda *args, tl=target_entries, idx=i: self.limit_length_to_1(tl, idx)

                if limit_to_1:
                    #tracks when sth is written  or deleted inside the box_variable so as to limit it's length
                    box_var.trace_add('write', limit_to_1)

                    #binding the release of a valid key to jumping to the next possible box
                    box_entry.bind('<KeyRelease>', lambda event, tl=target_entries, idx = i:
                    self.jump_to_nxt_entry(event, tl, idx))

                    #binding the release of a backspace key to jumping to the previous possible box
                    box_entry.bind('<KeyPress-BackSpace>', lambda event, tl= target_entries, idx = i:
                    self.reverse_jump(event, tl, idx))


            #only numbers should be allowed
            #only a digit per box is allowed
            #if next box is jumpable -> check for content inside the box ->jump to the next box

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
        type: str = label.lower()
        p_command = self.pin_submitted
        pin_vm = CodeInputViewModel(screen_type=type, label=label, command_on_click=p_command)
        return self.code_input_screen(pin_vm)

    def guess_input_screen(self,label: str ='GUESS'):
        type: str = label.lower()
        g_command = self.guess_submitted
        guess_vm = CodeInputViewModel(screen_type=type, label=label, command_on_click=g_command)
        return self.code_input_screen(guess_vm)


    def stats_screen(self) -> ttk.Frame:

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
        ...

    def game_over_screen(self):
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

        #inner frame where the player_outcome_frame, metrics_frame and brn_frame exists
        inner_frame = ttk.Frame(
            frame,
            style='TFrame'
        )
        inner_frame.grid(row=2, column=0, padx=10, sticky='nsew')

        #contains the winner and loser frames
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
        frame = ttk.Frame(
            master,
            style='TFrame'
        )

        leader_board_btn = ttk.Button(
            frame,
            text='LEADERBOARD',
            bootstyle = 'info-outline'
        )
        leader_board_btn.grid(row=0, column=0, padx=10, sticky='w')

        play_again_btn = ttk.Button(
            frame,
            text='PLAY AGAIN',
            bootstyle = 'success-outline'
        )
        play_again_btn.grid(row=0, column=1, padx=10, sticky='n')

        exit_btn = ttk.Button(
            frame,
            text='Exit',
            bootstyle = 'danger-link'
        )
        exit_btn.grid(row=0, column=2, padx=10, sticky='e')

        return frame

    def format_to_string(self, data: list[int]) -> str:
        return ' '.join(map(str, data))

    def game_metrics_label_frame(self, master: ttk.Frame):
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


    #methods callable by the presenter reference
    def display_error_popup(self, label: str , message: str):
        showwarning(title=f'INVALID {label}', message=message)


    def render_new_screen(self, vm: AppViewModel):
        self.home_frame.grid_forget()
        self.setup_frame.grid_forget()
        self.guess_frame.grid_forget()
        self.pin_frame.grid_forget()
        self.stats_frame.grid_forget()
        self.game_over_frame.grid_forget()

        # not sure if i should validate the details for emptiness

        if vm.screen  == GameScreen.NAME_SETUP:
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

    # handles updates to the different screens
    def update_code_frame_content(self, player_name: str, screen_type: str):
        if self.pin_title_label is None or self.guess_title_label is None:
            print('Error; The title frame is still None')

        new_text = f'WELCOME, {player_name.title()} 🤗'
        if screen_type.lower() == 'guess':
            self.guess_title_label.configure(text=new_text)
        else:
            self.pin_title_label.configure(text=new_text)

    def update_name_setup_index(self):
        if self.prompt_label_frame is None:
            print('Error; The name frame is still None')

        else:
            self.ui_player_index += 1
            new_text = f'PLAYER{self.ui_player_index}, ENTER A PLAYER NAME'
            self.prompt_label_frame.configure(text=new_text)

    def update_game_over_screen(self, details: GameOverDetails):
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
        if self.stats_inner_frame is None:
            print('Error; The stat main frame is still None')

        l_frames = []
        for i in range(len(sub_stats)):
            name_label_frame = NameLabel(self.stats_inner_frame, sub_stats[i])
            l_frames.append(name_label_frame)

        if len(l_frames) > 1:
            for i, label in enumerate(l_frames):
                label.frame.grid(row=2, column=i, padx=10, pady=10)
                label.frame.grid_columnconfigure(i, weight=1)
        else:
            l_frames[0].frame.grid(row=2, column=0, padx=10, pady=10)

    #event handlers of the view
    def mode_selected(self):
        self.presenter.create_player_sequence(self.player_mode.get())

    def name_entered(self):
        name = self.name_var.get()
        self.name_entry.delete(0, tk.END)
        self.presenter.store_name_sequence(name)

    def pin_submitted(self):
        pin_string = ''.join(p.get() for p in self.pin_enty if p.get())
        self.presenter.pin_submitted_sequence(pin_string)

        for p in self.pin_enty:
            p.delete(0, tk.END)

        if self.pin_enty: self.pin_enty[0].focus_set()


    def guess_submitted(self):
        guess_string = ''.join(g.get() for g in self.guess_enty if g.get())
        self.presenter.guess_submitted_sequence(guess_string)

        for g in self.guess_enty:
            g.delete(0, tk.END)

        if self.guess_enty: self.guess_enty[0].focus_set()


    def guess_again_clicked(self):
        self.presenter.guess_again_sequence()



# model = MainGameModel()
# view = GameView(model=model)
# view.start()