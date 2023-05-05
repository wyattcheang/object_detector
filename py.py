import os
import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

# specify the path of the directory to be read
path = "Image"

# create an empty list to store file names
file_names = []


attribute_names = ["image", "contrast", "brightness", "sigma", "size", "threshold", "maxval", "kernel"]


class Data:
    def __init__(self, image=None, kernel=None):
        self.image = image

    def is_complete(self):
        return self.require_data_complete

    def update_data(self, value, index):
        setattr(self, attribute_names[index], value)
        self.require_data_complete = all(
            getattr(self, attr) is not None for attr in vars(self) if not attr.startswith('__'))


def __str__(self):
        return f"Image path: {self.image}\n" \
               f"Contrast: {self.contrast}\n" \
               f"Brightness: {self.brightness}\n" \
               f"Sigma: {self.sigma}\n" \
               f"Size: {self.size}\n" \
               f"Threshold: {self.threshold}\n" \
               f"Maxval: {self.maxval}\n" \
               f"Kernel: {self.kernel}\n"


require_data = Data()

# iterate over each file in the directory
for filename in os.listdir(path):
    # check if the current file is a regular file (not a directory)
    if os.path.isfile(os.path.join(path, filename)):
        # add the file name to the list
        file_names.append(filename)


class ComboBoxFrame(ctk.CTkFrame):
    def __init__(self, master, titles, callback):
        super().__init__(master)

        self.comboboxes = []
        self.titles = titles if titles else []

        for i, title in enumerate(self.titles):
            # Create the label
            self.label = ctk.CTkLabel(self, text=title)
            self.label.grid(row=i, column=0, padx=(20, 0), pady=20, sticky="w")

            # Create the combobox
            combobox = ctk.CTkComboBox(self, values=[], state="readonly")
            combobox.grid(row=i, column=1, columnspan=2, padx=16, pady=10, sticky="w")
            combobox.configure(width=200)

            # Configure combobox event to a function that prints the selected value
            combobox.configure(command=lambda value, index=i: self.on_select(value, index))

            combobox.bind("<<ComboboxSelected>>", lambda event, cb=callback: cb())
            self.comboboxes.append((self.label, combobox))

    def on_select(self, value, index):
        global require_data
        control = self.comboboxes[index][0].cget(attribute_name="text")
        print(f"{control} {value}")
        if control == "Sharpening Kernel:":
            require_data.update_data(value, 7)
        if control == "Select your picture:":
            require_data.update_data(value, 0)
        print(require_data)
        print(require_data.is_complete())

    def set_values(self, values_list):
        for i, values in enumerate(values_list):
            self.comboboxes[i][1].configure(values=values)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.resizable(False, False)
        self.title("Image and Special Effect")
        self.geometry("1110x750")
        # self.grid_columnconfigure(1, weight=1)

        self.file_frame = ComboBoxFrame(self, titles=["Select your picture:"], callback=self.enable_button)
        self.file_frame.set_values([file_names])
        self.file_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.apply_button = ctk.CTkButton(self, text="Apply", command=self.button_event, state=ctk.DISABLED)
        self.apply_button.grid(row=6, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.apply_button.configure(height=50)

    def enable_button(self):
        print("called")
        if require_data.is_complete():
            self.apply_button.config(state='normal')
        else:
            self.apply_button.config(state='disabled')

    def button_event(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
