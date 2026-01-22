# # import tkinter as tk
# # from tkinter import ttk
# #
# #
# # class ScrollableTextApp:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Bound Scrollbar & Text Box")
# #
# #         self.builder()
# #
# #     def builder(self):
# #         # 1. Create a container frame
# #         frame = ttk.Frame(self.root, padding="10")
# #         frame.pack(expand=True, fill='both')
# #
# #         # 2. Create the Scrollbar
# #         self.scrollbar = ttk.Scrollbar(frame)
# #         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# #
# #         # 3. Create the Text Box
# #         self.text_box = tk.Text(frame,
# #                                 height=10,
# #                                 width=40,
# #                                 yscrollcommand=self.scrollbar.set)
# #         self.text_box.pack(side=tk.LEFT, expand=True, fill='both')
# #
# #         # 4. Link the Scrollbar back to the Text Box
# #         self.scrollbar.config(command=self.text_box.yview)
# #
# #         # UI Controls
# #         btn_frame = ttk.Frame(self.root, padding="5")
# #         btn_frame.pack(fill='x')
# #
# #         ttk.Button(btn_frame, text="Add Line", command=self.add_line).pack(side=tk.LEFT, padx=5)
# #         ttk.Button(btn_frame, text="Add History (List Comp)", command=self.add_history_batch).pack(side=tk.LEFT, padx=5)
# #         ttk.Button(btn_frame, text="Clear All", command=self.clear_text).pack(side=tk.LEFT, padx=5)
# #
# #     def add_line(self):
# #         """Adds content and automatically scrolls to the bottom."""
# #         line_count = int(self.text_box.index('end-1c').split('.')[0])
# #         new_content = f"Line {line_count}: Updating the bound view...\n"
# #
# #         # Insert at the end
# #         self.text_box.insert(tk.END, new_content)
# #         self.text_box.see(tk.END)
# #
# #     def add_history_batch(self):
# #         """
# #         ARCHITECT CHALLENGE: Refactoring your nested PIN logic
# #         into a single, high-speed List Comprehension.
# #         """
# #         pins = [[2, 1, 4, 5], [3, 6, 1, 8], [9, 0, 4, 2]]
# #         fdback = ['2dead 1inj', '3dead 0inj', '1dead 1inj']
# #
# #         # THE REFACTOR:
# #         # We transform the data and format the strings in ONE step.
# #         # Logic: Join digits as strings for every pin, then pair with feedback.
# #         formatted_history = [
# #             f"{''.join(str(d) for d in p):>8} {' ' * 20:<8} {f}\n"
# #             for p, f in zip(pins, fdback)
# #         ]
# #
# #         # Bulk insert into the View
# #         for entry in formatted_history:
# #             self.text_box.insert(tk.END, entry)
# #
# #         self.text_box.see(tk.END)
# #
# #     def clear_text(self):
# #         """Clears the text box; the scrollbar resets automatically."""
# #         self.text_box.delete('1.0', tk.END)
# #
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = ScrollableTextApp(root)
# #     root.mainloop()
#
# def structure_feedback_msg( feedback_msg: str, current_guess: list[int]):
#     structured_data = f'{''.join(str(d) for d in current_guess)} -  {feedback_msg}'
#     return structured_data
#
# msg = '2d and 1inj'
# guess = [3, 5, 7, 0]
#
# history_item = structure_feedback_msg(msg, guess)
# print(history_item)



def remove_spaces(my_list:list , index: int) -> int:
    content = my_list[index].strip()

    if len(content) == 0:
        del my_list[index]

    return len(my_list)

def limit_to_1(my_list:list , index: int):
    content = my_list[index].strip()

    if len(content) > 1:
        return content[:1]
    else:
        return content

def jump_to_new_entry( target_list, index):

    return None

def move_now(target_list, index: int):
    content = target_list[index].strip()

    #remove space from the particular value
    if len(content) == 0:
        del target_list[index]

    # limit the length of the value to 1
    if len(content) > 0 :
        content = content[:1]

    #jump to the new index and return it
    next_index = index + 1
    if 0 <= index and next_index < len(target_list):
        return target_list[next_index]
    return None

poss_list = [' 20','271', '400000', '1']




jump_trial = move_now(poss_list, 0)
print(jump_trial)