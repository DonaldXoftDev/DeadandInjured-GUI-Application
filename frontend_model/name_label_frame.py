import ttkbootstrap as ttk
import tkinter as tk
from typing import List, Dict

from game_presenter import RequiredDetails


class NameLabel:
    def __init__(self, master, details: RequiredDetails):
        self.details = details
        self.frame = ttk.LabelFrame(master,text=self.details.name.title(), labelanchor='nw')

        self.pin_vars = []
        self.details.guess = [1,9,3,2]
        self.guess_vars = []
        self.count_vars = []



        self.bio_frame = self.create_bio_frame()
        self.bio_frame.grid(row=0, column=0, padx=(10, 10), pady=10)
        self.bio_frame.grid_columnconfigure(0, weight=1)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)





    def create_bio_frame(self):
        frame = ttk.Frame(self.frame)

        pin_label_frame = self.create_pin_label_frame(frame)
        guess_label_frame = self.create_guess_label_frame(frame)
        feedback_label_frame = self.create_feedback_label_frame(frame)

        guess_count_label_frame = self.create_guess_count_label_frame(frame)


        pin_label_frame.grid(row=0, column=0, padx=10, pady=20)
        pin_label_frame.grid_columnconfigure(0, weight=1)

        guess_label_frame.grid(row=1, column=0, padx=10, pady=20)
        guess_label_frame.grid_columnconfigure(0, weight=1)

        feedback_label_frame.grid(row=2, column=0, padx=10, pady=10)
        feedback_label_frame.grid_columnconfigure(0, weight=1)



        guess_count_label_frame.grid(row=4, column=0, padx=10, pady=10)
        guess_count_label_frame.grid_columnconfigure(0, weight=1)

        return frame

    def toggle_switching(self, toggle_var):
        if toggle_var.get():
            for index, var in enumerate(self.pin_vars):
                var.set(self.details.guess[index])
        else:
            for var in self.pin_vars:
                var.set('⚫')

    def create_pin_boxes(self,frame, boot_style_color:str, entry_state, style:str, data,
                         start_row:int, var_list:list,  range_count:int):

        for i in range(range_count):
            box_var = tk.StringVar()
            box_entry = ttk.Entry(
                frame,
                textvariable=box_var,
                style=style,
                bootstyle=boot_style_color,
                state=entry_state,
                width= 5,
                justify='center'
            )

            box_entry.grid(row=start_row,column=i, padx=10, pady=10)
            var_list.append(box_var)

            if isinstance(data,list):
                box_var.set(data[i])
            elif data:
                box_var.set(str(data))

            frame.grid_columnconfigure(i, weight=1)


    def create_pin_label_frame(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame,text='YOUR PIN', labelanchor='nw')

        show_password = tk.BooleanVar(value=False)

        password_toggle = ttk.Checkbutton(frame, text='Show', variable=show_password,bootstyle='light-round-toggle')
        password_toggle.grid(row=0, column=3, columnspan=4, sticky='nsew')

        self.create_pin_boxes(frame,'primary','readonly','Pin.TEntry',
                              '⚫',1,self.pin_vars,4,)

        trace_callback = lambda *args, toggle_var=show_password: self.toggle_switching(toggle_var)

        show_password.trace_add('write', trace_callback)
        return frame

    def create_guess_label_frame(self,parent_frame):
        frame = ttk.LabelFrame(parent_frame,text='YOUR GUESS', labelanchor='nw')

        self.create_pin_boxes(frame,'primary','readonly','Pin.TEntry', self.details.guess,
                              0, var_list=self.guess_vars, range_count=4)

        return frame

    def create_feedback_label_frame(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text='HISTORY', labelanchor='n')

        history_widget = tk.Text(frame, height=5, width=22, font=('Helvetica', 15))
        history_widget.grid(row=0, column=0, sticky='nsew', padx=6, pady=10)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', bootstyle='round')
        scrollbar.grid(row=0, column=1, sticky='ns', pady=10)

        history_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=history_widget.yview)

        return frame

    def create_guess_count_label_frame(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text='GUESS COUNT', labelanchor='n')

        count_label_frame = self.create_count_frame(frame)

        count_label_frame.grid(row=0, column=0, padx=40, pady=10)
        count_label_frame.grid_columnconfigure(0, weight=1)

        return frame

    def create_count_frame(self, parent_frame):
        frame = ttk.Frame(parent_frame)

        guess_attempt = str(self.details.guess_count)
        string_count = len(guess_attempt)

        if string_count < 2:
            guess_attempt = '0' + guess_attempt

        count_list = [c for c in guess_attempt]

        self.create_pin_boxes(frame,'danger','readonly','Count.TEntry',
                              data=count_list,start_row=0,var_list=self.count_vars, range_count=len(guess_attempt))
        return frame


# window = ttk.Window(themename='superhero')
#
# players = [RequiredDetails('donald', state=None, turn=None), RequiredDetails('joe', state=None, turn=None)]
#
# for i in range(len(players)):
#     player_name_label = NameLabelFrame(window, players[i])
#     player_name_label.frame.grid(row=0, column=i, padx=10, pady=10)
#
# window.mainloop()


