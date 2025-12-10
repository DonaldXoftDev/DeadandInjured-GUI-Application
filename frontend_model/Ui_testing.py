from logic import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from frontend_model.game_model import GameModel
from frontend_model.game_controller import GameController




class DeadAndInjuredGUI:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        # self.interactions = Interactions()
        self.master.title("Dead&Injured GUI")

        self.entry_boxes = []
        self.entry_vars = []

        self.name_var = tk.StringVar()




        #style
        style = ttk.Style()
        self.label_font = ('Arial', 20)
        self.button_font =('Arial', 15)


        # #frame style
        # style.configure('TFrame',)


        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 15), )

        style.configure('TButton', font=('Helvetica', 12), padding=[40,10])

        style.configure('TLabelframe.Label', font=('Helvetica', 12), )

        style.configure('Pin.TEntry', font=('Helvetica', 12))
        style.configure('Count.TEntry', font=('Arial', 16), padding=10)

        # label style
        style.configure('TLabel', font=self.label_font)
        style.configure('name.TLabel', font=('Helvetica', 15))
        style.configure('name.TLabelFrame.Label', font=('Helvetica', 15))


        #entry style
        style.configure('TEntry', padding=10)


        #initializations
        self.main_frame = self.create_main_container()
        self.home_screen = self.create_home_screen()
        self.setup_frame = self.create_setup_screen()
        self.game_frame = self.create_game_screen()
        self.comp_frame = self.comp_screen()
        self.result_frame = self.result_frame()



        #place the main_frame on the window(self.master)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        #place the setup_frame inside the main_frame
        self.home_screen.grid(row=0, column=0, sticky = 'nsew')



        #center the frame inside the main_frame horizontally and vertically
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.master.mainloop()


    def create_main_container(self):
        frame = ttk.Frame(self.master,)
        return frame

    def move_to_set_up_screen(self):
            self.transition_to_new_screen(self.home_screen,self.setup_frame)


    def create_home_screen(self):
        frame = ttk.Frame(self.master,padding= 40)

        title_frame = ttk.Frame(frame)
        title_frame.grid(row=0, column=0, sticky='nsew')
        title_frame.grid_columnconfigure(0, weight=1)


        dead_title_label = ttk.Label(title_frame, text="Dead")
        dead_title_label.grid(row=0, column=0)
        rule_1 = ttk.Separator(title_frame, orient='horizontal')
        rule_1.grid(row=0, column=1,columnspan=4,sticky='ew',)

        and_title_label = ttk.Label(title_frame, text="And")
        and_title_label.grid(row=1, column=1)
        rule_2 = ttk.Separator(title_frame, orient='horizontal')
        rule_2.grid(row=1, column=2,columnspan=2,sticky='ew',)



        injured_title_label = ttk.Label(title_frame, text="Injured")
        injured_title_label.grid(row=2, column=2)
        rule_3 = ttk.Separator(title_frame, orient='horizontal')
        rule_3.grid(row=2, column=3,columnspan=1,sticky='ew',)

        menu_button = ttk.Menubutton(title_frame, text='Player Mode', bootstyle='info')
        menu_button.grid(row=3, column=3, columnspan=1,pady= 20)

        var= tk.StringVar()
        drop_menu = ttk.Menu(menu_button, tearoff=False)
        drop_menu.add_radiobutton(label='Player Vs Computer', variable=var, value='H_Vs_C')
        drop_menu.add_radiobutton(label='Player Vs Player', variable=var, value='H_Vs_H')

        menu_button['menu'] = drop_menu


        play_btn = ttk.Button(frame,text='PLAY GAME', bootstyle='danger',
                              command=self.move_to_set_up_screen)
        play_btn.configure(padding=[95,10],state=tk.DISABLED)
        play_btn.grid(row=1,column=0,pady=30)

        trace_back = lambda *args, mode_var=var,btn=play_btn: self.enable_btn(mode_var,btn)
        var.trace_add('write',trace_back)

        return frame


    def enable_btn(self, mode_var,btn):
        if mode_var.get():
            btn.configure(state='enabled')
            self.controller.create_players(mode_var.get())





    def create_setup_screen(self):
        frame = ttk.Frame(self.main_frame, style='TFrame', padding=100)

        outer_setup_container = ttk.Frame(frame,style='TFrame')
        outer_setup_container.grid(row=0, column=0, sticky='nsew')

        #center the input frame on the parent frame
        outer_setup_container.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(outer_setup_container, text="SETUP SCREEN", style='TLabel')
        title_label.grid(row=0, column=1, padx=60, pady=10)

        horiz_rule = ttk.Separator(outer_setup_container, orient='horizontal')
        horiz_rule.grid(row=1, column=0,columnspan=3, sticky='ew', padx=10, pady=(10,50))

        prompt_label_frame = ttk.LabelFrame(outer_setup_container, text='ENTER NAME', labelanchor='n')
        prompt_label_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        input_frame = ttk.Frame(prompt_label_frame, style='TFrame')
        input_frame.grid(row=0, column=0, sticky='nsew',padx=70, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=10, style='TEntry')
        name_entry.grid(row=0, column=1, padx=10, pady=30)
        name_entry.focus_set()



        submit_name_btn = ttk.Button(input_frame, text="SUBMIT",bootstyle= DANGER,
                                      command=self.store_player_name, padding=[40,10])

        submit_name_btn.grid(row=1, column=1, padx=10, pady=10)

        frame.grid_columnconfigure(0, weight=1)
        # frame.bind('<Enter>', self.store_player_name)

        return frame

    def limit_length_to_1(self,var_to_check):
        if len(var_to_check.get().strip()) > 1:
            var_to_check.set(var_to_check.get().strip()[:1])

        elif len(var_to_check.get().strip()) == 0:
            var_to_check.set(var_to_check.get().strip())



    def jump_to_new_entry(self,event):
        index = self.entry_boxes.index(event.widget)
        current_var = self.entry_vars[index]
        next_index = index + 1

        if next_index < len(self.entry_boxes) and len(current_var.get()) > 0:
            self.entry_boxes[next_index].focus()


    def reverse_jump(self,event):
        index = self.entry_boxes.index(event.widget)
        current_var = self.entry_vars[index]
        previous_index = index - 1

        if previous_index >= 0 and not current_var.get():
            self.entry_boxes[previous_index].focus()

    def handle_pin_or_guess_click(self):
        #
        # string_input_from_entry = ''
        # for var in self.entry_vars:
        #     string_input_from_entry += var.get()
        #
        # label = self.label.upper()
        # current_input_list = ''
        # if len(string_input_from_entry)  == 0:
        #     showerror(title='INVALID INPUT', message='YOU MUST ENTER A 4 DIGIT PIN')
        # else:
        #     if self.label.lower().strip() == 'guess':
        #         self.player_guess = validate_pin_or_guess(string_input_from_entry)
        #         current_input_list = self.player_guess
        #
        #     else:
        #         self.player_pin = validate_pin_or_guess(string_input_from_entry)
        #         current_input_list = self.player_pin
        #         self.controller.save_player_details(self.current_player, self.player_pin)
        #
        #
        #     if not current_input_list:
        #         showerror(title=f'INVALID {label}', message=f'{label} MUST CONTAIN UNIQUE DIGITS')
        #
        #     else:
        #         print(f'{label}: {current_input_list}')
        #         self.controller.save_player_details(self.current_player, self.player_pin)
        #         self.transition_to_new_screen(self.game_frame, self.result_frame)
        #
        #     for box in self.entry_vars:
        #         box.set('')
        # self.entry_boxes[0].focus()


    def create_game_screen(self, label='PIN'):
        frame = ttk.Frame(self.main_frame, style='TFrame', padding=50)



        title_label = ttk.Label(frame, text=f'WELCOME, {} 🤗', style='TLabel')
        title_label.grid(row=0, column=0,columnspan=3, padx=(10,200), pady=10)

        title_rule = ttk.Separator(frame, orient='horizontal')
        title_rule.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10, pady=(10,50))


        instruction_label_frame = ttk.LabelFrame(frame, text=f'Enter 4 digit unique {} from 0 to 9',
                                      style='name.TLabelFrame', labelanchor='n')
        instruction_label_frame.grid(row=2, column=0,columnspan=4, padx=10, pady=10)
        instruction_label_frame.grid_columnconfigure(0, weight=1)



        entry_frame = ttk.Frame(instruction_label_frame, style='TFrame', )
        entry_frame.grid(row=0, column=0,padx=50, pady=10, sticky='nsew')

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

            box_entry.grid(column=i , row=0,padx=10, pady=10)
            entry_frame.grid_columnconfigure(i, weight=1)


        submit_digits_btn = ttk.Button(entry_frame, text=f"CONFIRM {label.upper()}",bootstyle=SUCCESS,
                                       command=self.handle_pin_or_guess_click,padding=[50,10])
        submit_digits_btn.grid(row=1, column=0,columnspan=4, sticky='ew', padx=100, pady=40)

        return frame


    def comp_screen(self):
        frame = ttk.Frame(self.main_frame, style='TFrame', padding=100)
        comp_pin = computer_generate_pin()

        pin_label = ttk.Label(frame, text="COMPUTER HAS CHOOSEN PIN", style='TLabel')
        pin_label.grid(row=0, column=1,columnspan=4, padx=100, pady=40)

        is_guessing_label = ttk.Label(frame, text="YOU MUST GUESS", style='TLabel')
        is_guessing_label.grid(row=1, column=1,columnspan=4, padx=100, pady=100)

        frame.grid_columnconfigure(0, weight=1)
        return frame

    def return_to_guessing_page(self):
        new_screen = self.create_game_screen(label='Guess')
        self.transition_to_new_screen(self.result_frame, new_screen)


    def result_frame(self):
        frame = ttk.Frame(self.main_frame, style='TFrame',)

        main_frame = ttk.Frame(frame, style='TFrame')
        main_frame.grid(row=0, column=0, padx=10)

        title_label = ttk.Label(main_frame, text="STATS", )
        title_label.grid(row=0, column=0, padx=(10, 300))

        horizontal_divider = ttk.Separator(main_frame, orient='horizontal')
        horizontal_divider.grid(row=1, column=0, columnspan=6, sticky='ew', padx=10, pady=10)



        main_frame.grid_columnconfigure(1, weight=1)
        labels= []
        # for i in range(len(self.player_names)):
        #     name_label_frame = NameLabelFrame(main_frame, self.player_names[i])
        #     labels.append(name_label_frame)
        #
        # # labels.pop(0)
        # if len(labels) > 1:
        #     for i,label in enumerate(labels):
        #         label.frame.grid(row=2, column=i, padx=10, pady=10)
        #         label.frame.grid_columnconfigure(i, weight=1)
        # else:
        #     labels[0].frame.grid(row=2, column=0, padx=10, pady=10)


        guess_again_btn = ttk.Button(frame, text='GUESS AGAIN', bootstyle='success',
                                     command=self.return_to_guessing_page)

        guess_again_btn.grid(row=3, column=0, padx=50, pady=10)


        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        return frame

    def transition_to_new_screen(self, old_frame, new_frame):
        old_frame.grid_forget()
        new_frame.grid(row=0, column=0, sticky='nsew')
        self.entry_boxes[0].focus()


    def store_player_name(self,event=None):

        self.transition_to_new_screen(self.setup_frame, self.game_frame)
        # focus the mouse on the first box after transition
        self.entry_boxes[0].focus()


window= ttk.Window(themename='superhero')
window.grid(baseWidth=10, baseHeight=10, widthInc=10, heightInc=10)


game_model = GameModel()

game_controller = GameController(game_model)
dead_and_injured_logic = DeadAndInjuredGUI(window, game_controller)


