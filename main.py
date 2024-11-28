# - - - - - - - - - - - - - - - - 
#       Made by KynNotKien       
# - - - - - - - - - - - - - - - - 

# Please instal pandas before run my program
# pip install pandas

import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import pandas as pd
from tkinter import filedialog

# Color pattle
DARK_GREY = "#A7A7A7"
OFF_WHITE = "#F8F8FF"
BLACK = "#000000"

# Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Files Path
BASE_PATH = Path("Files/")
FILE_PATH =  BASE_PATH/"test.csv"

# Screen Class
class Screen:
    def __init__(self, root):
        self.root = root

        # Screen attributes
        self.root.title("Student Grade Management System")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        self.root.iconbitmap("logo.ico")

        # Title
        self.title = tk.Label(root, text="Student Grade Management System", font=("Arial", 20, "bold"), pady=10)
        self.description = tk.Label(root, text="Made by KynNotKien <3", pady=-10)
        self.title.pack()
        self.description.pack()

# Table Class
class Table(tk.Frame):
    def __init__(self, parent, room):
        super().__init__(parent)
        self.room = room
        self.pack(fill=tk.X, padx=10, pady=10, side=tk.RIGHT)

        # Create a fixed-size frame to contain the table
        self.table_frame = tk.Frame(self, width=900, height=500)
        self.table_frame.pack(expand=False)
        self.table_frame.pack_propagate(False)

        # Load data from CSV
        self.df = pd.read_csv(FILE_PATH)

        # Create Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=list(self.df.columns), show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.Y)

        # Configure columns
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=94, stretch=True, anchor=tk.CENTER)

        # Add data to Treeview
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

        self.tree.bind("<ButtonRelease-1>", self.on_select)

    # Get selected record information
    def on_select(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]

            # Update each entry in the entries
            labels = ['Name:', 'Age:', 'Maths:', 'Science:', 'English:',
                      'Social:', 'Computer:']
            for label, value in zip(labels, record):
                if label in self.room.entries:
                    self.room.entries[label].delete(0, tk.END)
                    self.room.entries[label].insert(0, value)

    # Update/edit table
    def update_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Reload data
        self.df = pd.read_csv(FILE_PATH)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    # Search record (by name)
    def search(self, search_term):
        # Filter the data based on the search term
        filtered_data = self.df[self.df['Name'].str.contains(search_term, case=False, na=False)]
        self.populate_table(filtered_data)

    # Fill records
    def populate_table(self, data_frame):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Add filtered data to Treeview
        for _, row in data_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))

# Room Class(controler)
class Room(tk.Frame):
    def __init__(self, parent, table):
        super().__init__(parent)
        self.entries = {}
        self.table = table
        self.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)

        # Configure frame
        self.configure(bg=DARK_GREY)
        self.pack_propagate(False)
        self.configure(width=300, height=600)

        # Search Section
        self.search_frame = tk.Frame(self, bg=DARK_GREY)
        self.search_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        self.search_entry = tk.Entry(self.search_frame, width=24, font=("Helvetica", 10))
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_record)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_search_button = tk.Button(self.search_frame, text="Clear", command=self.clear_search)
        self.clear_search_button.grid(row=0, column=2, padx=5, pady=5)

        # Create entry fields
        self.edit_frame = tk.Frame(self, bg=DARK_GREY)
        self.edit_frame.pack(side=tk.TOP, padx=10, fill=tk.X)

        labels = ['Name:', 'Age:', 'Maths:', 'Science:', 'English:',
                  'Social:', 'Computer:']

        for i, label in enumerate(labels):
            tk.Label(self.edit_frame, bg=DARK_GREY, text=label, font=("Helvetica", 10)).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            entry = tk.Entry(self.edit_frame, width=30, font=("Helvetica", 10))
            entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
            self.entries[label] = entry

        # Buttons Section
        self.button_frame = tk.Frame(self, bg=DARK_GREY)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

        tk.Button(self.button_frame, text="Add", width=10, command=self.add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Update", width=10, command=self.update_record).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete", width=10, command=self.delete_record).pack(side=tk.LEFT, padx=5)

        # File management panel
        self.file_manage = tk.Frame(self, bg=DARK_GREY)
        self.file_manage.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.file_list = tk.Listbox(self, width=50, height=10, font=("Helvetica", 10))
        self.file_list.pack(side=tk.LEFT, padx=10, pady=5)

        tk.Button(self.file_manage, text="Create File", width=10, command=self.create_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self.file_manage, text="Delete File", width=10, command=self.delete_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self.file_manage, text="Open File", width=10, command=self.open_file).pack(side=tk.LEFT, padx=5)

        self.load_files()
        

    # Get average mark, grade
    def calculate_average_and_grade(self):
        # Get the marks for the subjects
        try:
            maths = float(self.entries['Maths:'].get())
            science = float(self.entries['Science:'].get())
            english = float(self.entries['English:'].get())
            social = float(self.entries['Social:'].get())
            computer = float(self.entries['Computer:'].get())
        # If the entries not match data type => show message
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all subjects!")
            return None, None
        # Calculate the average
        average = (maths + science + english + social + computer) / 5
        # Determine grade based on average
        if average >= 90:
            grade = 'A'
        elif average >= 80:
            grade = 'B'
        elif average >= 70:
            grade = 'C'
        elif average >= 60:
            grade = 'D'
        else:
            grade = 'F'
        return average, grade

    # Add record
    def add_record(self):
        # Error Handling for empty fields
        if self.entries['Name:'].get() == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if self.entries['Age:'].get() == "":
            messagebox.showerror("Error", "Age cannot be empty")
            return
        if self.entries['Maths:'].get() == "":
            messagebox.showerror("Error", "Maths cannot be empty")
            return
        if self.entries['Science:'].get() == "":
            messagebox.showerror("Error", "Science cannot be empty")
            return
        if self.entries['English:'].get() == "":
            messagebox.showerror("Error", "English cannot be empty")
            return
        if self.entries['Social:'].get() == "":
            messagebox.showerror("Error", "Social cannot be empty")
            return
        if self.entries['Computer:'].get() == "":
            messagebox.showerror("Error", "Computer cannot be empty")
            return

        # Calculate Average and Grade
        average, grade = self.calculate_average_and_grade()
        if average is None or grade is None:
            return  # Exit if calculation failed

        # Write values to CSV file, including Average and Grade
        with open(FILE_PATH, "a", newline='') as file:
            values = [self.entries[label].get() for label in ['Name:', 'Age:', 'Maths:', 'Science:', 'English:', 'Social:', 'Computer:']]
            values.append(str(average))
            values.append(grade)
            file.write(",".join(values) + "\n")

        # Refresh the table
        self.table.update_table()

    # Update/edit record
    def update_record(self):
        selected_item = self.table.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No record selected!")
            return

        # Calculate Average and Grade
        average, grade = self.calculate_average_and_grade()
        if average is None or grade is None:
            return  # Exit if calculation failed

        updated_data = [self.entries[label].get() for label in self.entries if label != 'Average:' and label != 'Grade:']
        updated_data.extend([str(average), grade])

        # Read CSV data
        data = pd.read_csv(FILE_PATH)

        selected_values = self.table.tree.item(selected_item[0])["values"]
        selected_id = selected_values[0]  # Assuming ID is the first column in the Treeview

        # Check data and update record
        match_found = False
        for index, row in data.iterrows():
            if str(row.iloc[0]) == str(selected_id):
                data.iloc[index] = updated_data
                match_found = True
                break

        if not match_found:
            # Send error if user didnt select a record to update
            messagebox.showerror("Error", "Record not found!") 

        # Save the updated CSV file
        data.to_csv(FILE_PATH, index=False) 

        # Refresh the table
        self.table.update_table() 

    # Delete record
    def delete_record(self):
        selected_item = self.table.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "No record selected!")
            return

        selected_values = self.table.tree.item(selected_item[0])["values"]
        selected_id = selected_values[0]

        data = pd.read_csv(FILE_PATH)
        data = data[data.iloc[:, 0] != selected_id]
        data.to_csv(FILE_PATH, index=False)

        self.table.tree.delete(selected_item[0])
        self.table.update_table()

    # Search record button command
    def search_record(self):
        search_term = self.search_entry.get()
        if search_term:
            self.table.search(search_term)

    # Clear record button (give the record back)
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.table.update_table()

    # Load files from folder
    def load_files(self):
        self.file_list.delete(0, tk.END)
        for file in BASE_PATH.glob("*.csv"):
            self.file_list.insert(tk.END, file.name)

    # Create a new CSV file
    def create_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_name:
            # Create an empty CSV file with headers
            headers = ["Name", "Age", "Maths", "Science", "English", "Social", "Computer", "Average", "Grade"]
            with open(file_name, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            self.load_files()
    
    # Deleted selected file
    def delete_file(self):
        selected_file = self.file_list.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        file_path = BASE_PATH / selected_file
        if file_path.exists():
            file_path.unlink()
            self.load_files()
        else:
            messagebox.showerror("Error", "File does not exist!")

    # Open selected file and load into the table
    def open_file(self):
        selected_file = self.file_list.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        file_path = BASE_PATH / selected_file
        if file_path.exists():
            global FILE_PATH
            FILE_PATH = file_path
            self.table.update_table()
        else:
            messagebox.showerror("Error", "File does not exist!")
    

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = Screen(root)
    room = Room(root, None)
    table = Table(root, room)
    room.table = table
    root.mainloop()