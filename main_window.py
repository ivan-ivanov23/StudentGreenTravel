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

        # Create a button to calculate emissions at center of frame
        self.button = customtkinter.CTkButton(master=self.frame, text="Calculate Emissions", command=self.calculate_emissions)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        # Create a button to browse for a file at bottom of frame
        self.button = customtkinter.CTkButton(master=self.frame, text="Browse", command=self.button_click)
        self.button.grid(row=2, column=0, padx=10, pady=10)




    # add methods to app
    def button_click(self):
        # Make the button open file explorer for excel files only so that it is utf-8 encoded
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
            df = pd.read_excel(file.name, engine='openpyxl')
            # Display the name of the file that was selected
            self.label = customtkinter.CTkLabel(master=self.frame, text=f"Selected file: {os.path.basename(file.name)}",text_color="white", font=('Arial', 15), bg_color="transparent")
            self.label.grid(row=3, column=0, padx=10, pady=10)

    # function to call emissions.py and display a dataframe with the results
    def calculate_emissions(self):
        # Open new window on top of the main window
        self.new_window = customtkinter.CTkToplevel(self)
        self.new_window.title("Emissions Results")
        self.new_window.geometry("800x600")
        self.new_window.grid_columnconfigure(0, weight=1)

        # Create a label for the new window
        self.label = customtkinter.CTkLabel(self.new_window, text="Emissions Results",text_color="white", font=('Arial', 30))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Create a pandas dataframe to display the results
        data = {'Postcode': ['AB10', 'AB11', 'AB12', 'AB13', 'AB14'],
                'Emissions (kgCO2e)': [10, 20, 30, 40, 50]}
        df = pd.DataFrame(data)
        # Create a table to display the dataframe
        self.table = tkinter.ttk.Treeview(self.new_window, columns=list(df.columns), show="headings")
        self.table.grid(row=1, column=0, padx=20, pady=20)

        # Add the columns to the table
        for col in df.columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")
        # Add the data to the table
        for index, row in df.iterrows():
            self.table.insert("", "end", values=list(row))

            

                


# Run the app
app = App()
app.mainloop()
