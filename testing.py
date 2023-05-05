import tkinter as tk
from tkinter import ttk


class DynamicComboFrame(tk.Frame):
    def __init__(self, parent, num_combos):
        super().__init__(parent)

        self.combos = []

        for i in range(num_combos):
            combo = ttk.Combobox(self)
            combo.pack()
            combo.bind("<<ComboboxSelected>>", self.check_combos)
            self.combos.append(combo)

    def check_combos(self, event=None):
        all_selected = all(combo.get() for combo in self.combos)
        self.master.check_button_state(all_selected)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.dynamic_frame = DynamicComboFrame(self, 3)
        self.dynamic_frame.pack()

        self.button = tk.Button(self, text="Button", state="disabled")
        self.button.pack()

    def check_button_state(self, all_selected):
        if all_selected:
            self.button.configure(state="normal")
        else:
            self.button.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
