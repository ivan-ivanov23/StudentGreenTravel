import os
import pandas as pd
import customtkinter, tkinter
from tkinter.filedialog import askopenfile


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Student Emissions")
        self.grid_columnconfigure(0, weight=1)

        # add widgets to app
        self.label = customtkinter.CTkLabel(self, text="Student Emissions Tool",text_color="white", font=('Arial', 30))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.frame = customtkinter.CTkFrame(self, width=500, height=400, corner_radius=20)
        # Make the frame fill almost the entire window
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

        self.label = customtkinter.CTkLabel(master=self.frame, text="Select a Spreadsheet",text_color="white", font=('Arial', 15), bg_color="transparent")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Create a button to browse for a file at bottom of frame
        self.button = customtkinter.CTkButton(master=self.frame, text="Browse", command=self.button_click)
        self.button.grid(row=1, column=0, padx=10, pady=10)


    # add methods to app
    def button_click(self):
        # Make the button open file explorer for excel files only so that it is utf-8 encoded
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
            df = pd.read_excel(file.name, engine='openpyxl')
            print(df)        

# Run the app
app = App()
app.mainloop()
