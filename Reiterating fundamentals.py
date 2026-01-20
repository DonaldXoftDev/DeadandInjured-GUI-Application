# import tkinter as tk
# from tkinter import ttk
#
#
# class ScrollableTextApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Bound Scrollbar & Text Box")
#
#         self.builder()
#
#     def builder(self):
#         # 1. Create a container frame
#         frame = ttk.Frame(self.root, padding="10")
#         frame.pack(expand=True, fill='both')
#
#         # 2. Create the Scrollbar
#         self.scrollbar = ttk.Scrollbar(frame)
#         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
#         # 3. Create the Text Box
#         self.text_box = tk.Text(frame,
#                                 height=10,
#                                 width=40,
#                                 yscrollcommand=self.scrollbar.set)
#         self.text_box.pack(side=tk.LEFT, expand=True, fill='both')
#
#         # 4. Link the Scrollbar back to the Text Box
#         self.scrollbar.config(command=self.text_box.yview)
#
#         # UI Controls
#         btn_frame = ttk.Frame(self.root, padding="5")
#         btn_frame.pack(fill='x')
#
#         ttk.Button(btn_frame, text="Add Line", command=self.add_line).pack(side=tk.LEFT, padx=5)
#         ttk.Button(btn_frame, text="Add History (List Comp)", command=self.add_history_batch).pack(side=tk.LEFT, padx=5)
#         ttk.Button(btn_frame, text="Clear All", command=self.clear_text).pack(side=tk.LEFT, padx=5)
#
#     def add_line(self):
#         """Adds content and automatically scrolls to the bottom."""
#         line_count = int(self.text_box.index('end-1c').split('.')[0])
#         new_content = f"Line {line_count}: Updating the bound view...\n"
#
#         # Insert at the end
#         self.text_box.insert(tk.END, new_content)
#         self.text_box.see(tk.END)
#
#     def add_history_batch(self):
#         """
#         ARCHITECT CHALLENGE: Refactoring your nested PIN logic
#         into a single, high-speed List Comprehension.
#         """
#         pins = [[2, 1, 4, 5], [3, 6, 1, 8], [9, 0, 4, 2]]
#         fdback = ['2dead 1inj', '3dead 0inj', '1dead 1inj']
#
#         # THE REFACTOR:
#         # We transform the data and format the strings in ONE step.
#         # Logic: Join digits as strings for every pin, then pair with feedback.
#         formatted_history = [
#             f"{''.join(str(d) for d in p):>8} {' ' * 20:<8} {f}\n"
#             for p, f in zip(pins, fdback)
#         ]
#
#         # Bulk insert into the View
#         for entry in formatted_history:
#             self.text_box.insert(tk.END, entry)
#
#         self.text_box.see(tk.END)
#
#     def clear_text(self):
#         """Clears the text box; the scrollbar resets automatically."""
#         self.text_box.delete('1.0', tk.END)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ScrollableTextApp(root)
#     root.mainloop()

def structure_feedback_msg( feedback_msg: str, current_guess: list[int]):
    structured_data = f'{''.join(str(d) for d in current_guess)} -  {feedback_msg}'
    return structured_data

msg = '2d and 1inj'
guess = [3, 5, 7, 0]

history_item = structure_feedback_msg(msg, guess)
print(history_item)