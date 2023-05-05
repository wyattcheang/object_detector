import os
from abc import ABC

import PIL
import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

# specify the path of the directory to be read
path = "Image"

# create an empty list to store file names
file_names = []

# List to hold the attribute names in order
attribute_names = ["image",
                   "contrast", "brightness",
                   "kernel", "sigma", "size",
                   "morphology", "m_iteration",
                   "threshold", "maxval"]

# iterate over each file in the directory
for filename in os.listdir(path):
    # check if the current file is a regular file (not a directory)
    if os.path.isfile(os.path.join(path, filename)):
        # add the file name to the list
        file_names.append(filename)


# print the list of file names
# print(file_names)


class Data:
    def __init__(self):
        self.image = None
        self.contrast = False
        self.brightness = 12
        self.kernel = None
        self.sigma = 12
        self.size = 12
        self.morphology = None
        self.m_iteration = 0
        self.threshold = 127
        self.maxval = 127

    def is_complete(self):
        return all(getattr(self, attr) is not None for attr in vars(self) if not attr.startswith('__'))

    def update_data(self, value, index):
        setattr(self, attribute_names[index], value)

    def __str__(self):
        return f"Image path: {self.image}\n" \
               f"Contrast: {self.contrast}\n" \
               f"Brightness: {self.brightness}\n" \
               f"Kernel: {self.kernel}\n" \
               f"Sigma: {self.sigma}\n" \
               f"Size: {self.size}\n" \
               f"Morphology Operation: {self.morphology}\n" \
               f"Iteration: {self.m_iteration}\n" \
               f"Threshold: {self.threshold}\n" \
               f"Maxval: {self.maxval}\n"


require_data = Data()


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, titles):
        super().__init__(master)

        self.buttons = []
        self.titles = titles if titles else []

        for i, title in enumerate(self.titles):
            # Create the Buttons
            self.button = ctk.CTkButton(self, text=title, command=lambda index=i: self.button_event(index))
            self.button.grid(row=i, column=1, columnspan=2, padx=16, pady=16, sticky="w")
            self.buttons.append(self.button)

    def button_event(self, index):
        pass


class ComboBoxFrame(ctk.CTkFrame):
    def __init__(self, master, titles, callback):
        super().__init__(master)

        self.comboboxes = []
        self.titles = titles if titles else []
        self.callback = callback

        for i, title in enumerate(self.titles):
            # Create the label
            self.label = ctk.CTkLabel(self, text=title)
            self.label.grid(row=i, column=0, padx=(20, 0), pady=16, sticky="w")

            # Create the combobox
            combobox = ctk.CTkComboBox(self, values=[], state="readonly")
            combobox.grid(row=i, column=1, columnspan=2, padx=16, pady=16, sticky="w")
            combobox.configure(width=200)

            # Configure combobox event to a function that prints the selected value
            combobox.configure(command=lambda value, index=i: self.on_select(value, index, self.callback))

            self.comboboxes.append((self.label, combobox))

    def on_select(self, value, index, callback):
        global require_data
        control = self.comboboxes[index][0].cget(attribute_name="text")
        print(f"{control} {value}")
        if control == "Image:":
            require_data.update_data(value, 0)
        if control == "Sharpening Kernel:":
            require_data.update_data(value, 3)
        if control == "Morphology Operation:":
            require_data.update_data(value, 6)
        print(require_data)
        print(require_data.is_complete())
        callback()

    def set_values(self, values_list):
        for i, values in enumerate(values_list):
            self.comboboxes[i][1].configure(values=values)


class SwitchFrame(ctk.CTkFrame):
    def __init__(self, master, titles):
        super().__init__(master)
        self.switches = []
        self.titles = titles if titles else []

        for i, title in enumerate(self.titles):
            # Create the label
            self.label = ctk.CTkLabel(self, text=title)
            self.label.grid(row=i, column=0, padx=20, pady=16, sticky="w")
            self.label.columnconfigure(0, minsize=66)

            # Create the switch
            switch_value = ctk.BooleanVar(value=False)
            self.switch = ctk.CTkSwitch(self, text="", variable=switch_value,
                                        command=lambda index=i: self.switch_event(switch_value.get(), index))
            self.switch.grid(row=i, column=1, columnspan=2, padx=10, pady=10, sticky="w")
            self.switches.append((self.label, self.switch))

    def switch_event(self, value, index):
        control = self.switches[index][0].cget(attribute_name="text")
        print(f"{control}: {value}")
        if control == "Contrast":
            require_data.update_data(value, 1)


class SliderFrame(ctk.CTkFrame):
    def __init__(self, master, values, min_value, max_value):
        super().__init__(master)

        self.sliders = []
        self.values = values if values else []
        self.min = min_value
        self.max = max_value

        for i, value in enumerate(self.values):
            # Create the label
            self.label = ctk.CTkLabel(self, text=value)
            self.label.grid(row=i, column=0, padx=20, pady=16, sticky="w")
            self.label.columnconfigure(0, minsize=66)

            # Create the slider
            self.slider = ctk.CTkSlider(self, from_=self.min, to=self.max, number_of_steps=max_value - min_value,
                                        command=lambda val, index=i: self.slider_event(val, index))
            self.slider.grid(row=i, column=1, padx=0, pady=16, sticky="w")

            # Create the value label
            self.value_label = ctk.CTkLabel(self, text=str(int(self.slider.get())))
            self.value_label.grid(row=i, column=2, padx=20, pady=16)
            self.value_label.configure(width=30)

            # Store the value_label as an attribute of the slider object
            self.sliders.append((self.label, self.slider, self.value_label))

    def slider_event(self, value, index):
        # Update the value label of the slider
        global require_data
        control = (self.sliders[index][0].cget(attribute_name="text"))
        print(f"{control}: {value}")
        self.sliders[index][2].configure(text=str(int(value)))
        if control == "Brightness":
            require_data.update_data(int(value), 2)
        if control == "Sigma":
            require_data.update_data(int(value), 4)
        if control == "Size":
            require_data.update_data(int(value), 5)
        if control == "Iteration":
            require_data.update_data(int(value), 7)
        if control == "Threshold":
            require_data.update_data(int(value), 8)
        if control == "Max value":
            require_data.update_data(int(value), 9)

    def get(self):
        slider_values = []
        for _, return_value, _ in self.sliders:
            slider_values.append(return_value)
        return slider_values


class TabFrame(ctk.CTkTabview, ABC):
    def __init__(self, master, titles):
        super().__init__(master)
        self.titles = titles
        self.images = []

        # create tabs
        for i, value in enumerate(self.titles):
            self.add(str(value))
            self.label = ctk.CTkLabel(master=self.tab(str(value)), text="")
            self.label.pack(side="top", fill="both", padx=10, pady=10, expand=True)
            self.images.append(self.label)

    def set_image(self, image, index):
        # convert the image from OpenCV to PIL format
        image = PIL.Image.fromarray(image)
        # convert the PIL image to a Tkinter PhotoImage and display it
        photo = PIL.ImageTk.PhotoImage(image)
        self.images[index].configure(image=photo)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.resizable(False, False)
        self.title("Image and Special Effect")
        self.columnconfigure(1, minsize=660)
        self.columnconfigure(2, minsize=350)
        # self.grid_columnconfigure(1, weight=1)

        self.file_frame = ComboBoxFrame(self, titles=["Image:"], callback=self.enable_button)
        self.file_frame.set_values([file_names])
        self.file_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.bright_contrast_frame = ctk.CTkFrame(self)
        self.bright_contrast_frame.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.bright_contrast_frame.configure(fg_color="transparent")

        self.contrast_frame = SwitchFrame(self.bright_contrast_frame, titles=["Contrast"])
        self.contrast_frame.grid(row=0, column=0, sticky="nsew")
        self.contrast_frame.configure(fg_color="transparent")

        self.bright_frame = SliderFrame(self.bright_contrast_frame, min_value=0, max_value=25, values=["Brightness"])
        self.bright_frame.grid(row=1, column=0, sticky="nsew")
        self.bright_frame.configure(fg_color="transparent")

        self.noise_reduction_sharpen_frame = ctk.CTkFrame(self)
        self.noise_reduction_sharpen_frame.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.sharpen_frame = ComboBoxFrame(self.noise_reduction_sharpen_frame, titles=["Sharpening Kernel:"],
                                           callback=self.enable_button)
        self.sharpen_frame.set_values([["None", "Laplacian Kernel", "Un-sharp Masking Kernel"]])
        self.sharpen_frame.grid(row=0, column=0, sticky="nsew")
        self.sharpen_frame.configure(fg_color="transparent")
        self.noise_frame = SliderFrame(self.noise_reduction_sharpen_frame, min_value=0, max_value=25,
                                       values=["Sigma", "Size"])
        self.noise_frame.grid(row=1, column=0, sticky="nsew")
        self.noise_frame.configure(fg_color="transparent")

        self.morphology_operation_frame = ctk.CTkFrame(self)
        self.morphology_operation_frame.grid(row=3, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.morphology_operation_frame.configure(fg_color="transparent")

        self.morphology_type_frame = ComboBoxFrame(self.morphology_operation_frame, titles=["Morphology Operation:"],
                                                   callback=self.enable_button)
        self.morphology_type_frame.set_values([["None", "Erosion", "Dilation", "Opening", "Closing"]])
        self.morphology_type_frame.grid(row=0, column=0, sticky="nsew")
        self.morphology_type_frame.configure(fg_color="transparent")

        self.morphology_iteration_frame = SliderFrame(self.morphology_operation_frame, min_value=0, max_value=5, values=["Iteration"])
        self.morphology_iteration_frame.grid(row=1, column=0, sticky="nsew")
        self.morphology_iteration_frame.configure(fg_color="transparent")

        self.threshold_frame = SliderFrame(self, min_value=0, max_value=255, values=["Threshold", "Max value"])
        self.threshold_frame.grid(row=4, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.apply_button = ctk.CTkButton(self, text="Apply", command=self.button_event, state=ctk.DISABLED)
        self.apply_button.grid(row=5, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew")
        self.apply_button.configure(height=50)

        # set the callback function for the combobox
        self.file_frame.bind("<<ComboboxSelected>>", self.enable_button)
        self.sharpen_frame.bind("<<ComboboxSelected>>", self.enable_button)

        self.image_frame = TabFrame(self, ["Org", "Grey",
                                           "B&C",
                                           "NR&S",
                                           "MO",
                                           "Contours"])
        self.image_frame.grid(row=0, column=1, rowspan=6, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.grid(row=0, column=2, rowspan=6, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.result_label = ctk.CTkLabel(self.result_frame, text="Result")
        self.result_label.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))


    def enable_button(self):
        print("called")
        if require_data.is_complete():
            print("hi")
            self.apply_button.configure(state='normal')
        else:
            self.apply_button.configure(state='disabled')

    def button_event(self):
        global require_data
        print("Clicked!")
        print(require_data)
        process(self.image_frame)


def process(frame):
    areas = []
    perimeters = []
    image = cv2.imread("Image/" + require_data.image)

    # Define the maximum width
    max_width = 600

    # Calculate the scale factor based on the maximum width
    scale_factor = max_width / image.shape[1]

    # Calculate the new height based on the scale factor
    new_height = int(image.shape[0] * scale_factor)

    # Resize the image
    resized_img = cv2.resize(image, (max_width, new_height))

    org_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    gry_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    frame.set_image(org_img, 0)
    frame.set_image(gry_img, 1)

    modified1_img = brightness_contrast(gry_img)
    modified2_img = noise_reduction_and_sharpening(modified1_img)
    frame.set_image(modified1_img, 2)
    frame.set_image(modified2_img, 3)

    morph_img = morphology(modified2_img)
    frame.set_image(morph_img, 4)

    cont_img = contour_hierarchy(org_img, morph_img, areas, perimeters)
    frame.set_image(cont_img, 5)
    print(areas)
    print(perimeters)


def brightness_contrast(img):
    # Adjust the Brightness
    alpha = 1 + (require_data.brightness * 10) / 255
    result = cv2.addWeighted(img, alpha, img, 0, 0)

    # Adjust the Contrast
    if require_data.contrast:
        result = cv2.equalizeHist(result)

    return result


def noise_reduction_and_sharpening(img):
    if require_data.size % 2 == 0:
        require_data.size += 1

    blur_img = cv2.GaussianBlur(img, (require_data.size, require_data.size), require_data.sigma)
    result = blur_img
    if require_data.kernel == 1:
        laplacian_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        result = cv2.filter2D(blur_img, -1, laplacian_kernel)
    elif require_data.kernel == 2:
        unsharp_masking_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        result = cv2.filter2D(blur_img, -1, unsharp_masking_kernel)
    return result


def contour_hierarchy(org_img, gry_img, areas, perimeters):
    thresh_value, thresh_img = cv2.threshold(gry_img, require_data.threshold, require_data.maxval, type=cv2.THRESH_BINARY)
    cont, heir = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, c in enumerate(cont):
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        if area >= 1000:
            areas.append(area)
        if perimeter >= 1000:
            perimeters.append(cv2.arcLength(c, True))
        cv2.drawContours(org_img, cont, i, (0, 255, 0), 2)

    return org_img


def morphology(img):
    mo = require_data.morphology
    iterations = require_data.m_iteration
    ker = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    if mo == "None":
        return img
    elif mo == "Erosion":
        return cv2.morphologyEx(img, cv2.MORPH_ERODE, ker, iterations)
    elif mo == "Dilation":
        return cv2.morphologyEx(img, cv2.MORPH_DILATE, ker, iterations)
    elif mo == "Opening":
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, ker, iterations)
    elif mo == "Closing":
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, ker, iterations)


if __name__ == "__main__":
    app = App()
    app.mainloop()
