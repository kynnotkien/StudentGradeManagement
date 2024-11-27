#-----------------------
# Made by KynNotKien <3
#-----------------------

# Please install pandas!
# pip install pandas

import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import pandas as pd

# Colors
DARK_GREY = "#979797"
OFF_WHITE = "#F8F8FF"
BLACK = "#000000"

# Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Files Path
FILE_PATH = Path(__file__).parent / "test.csv"

# Screen Class
class Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Management System")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)

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

        # Create scrollbars
        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

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

    def on_select(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]

            # Update each entry in the Room
            labels = ['Name:', 'Age:', 'Maths:', 'Science:', 'English:',
                      'Social:', 'Computer:']
            for label, value in zip(labels, record):
                if label in self.room.entries:
                    self.room.entries[label].delete(0, tk.END)
                    self.room.entries[label].insert(0, value)

    def update_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reload data from CSV
        self.df = pd.read_csv(FILE_PATH)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))


# Room Class
class Room(tk.Frame):
    def __init__(self, parent, table):
        super().__init__(parent)
        self.entries = {}
        self.table = table
        self.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)

        # Configure frame
        self.configure(bg=DARK_GREY)
        self.pack_propagate(False)
        self.configure(width=300, height=500)

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

        # Buttons
        self.button_frame = tk.Frame(self, bg=DARK_GREY)
        self.button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        tk.Button(self.button_frame, text="Add", command=self.add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Update", command=self.update_record).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete", command=self.delete_record).pack(side=tk.LEFT, padx=5)

    def calculate_average_and_grade(self):

        # Get the marks for the subjects
        try:
            maths = float(self.entries['Maths:'].get())
            science = float(self.entries['Science:'].get())
            english = float(self.entries['English:'].get())
            social = float(self.entries['Social:'].get())
            computer = float(self.entries['Computer:'].get())
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

        match_found = False
        for index, row in data.iterrows():
            if str(row.iloc[0]) == str(selected_id):
                data.iloc[index] = updated_data
                match_found = True
                break

        if not match_found:
            messagebox.showerror("Error", "Record not found!")

        # Save the updated CSV file
        data.to_csv(FILE_PATH, index=False)

        # Refresh the table
        self.table.update_table()

    # Delete record
    def delete_record(self):
        pass

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = Screen(root)
    room = Room(root, None)
    table = Table(root, room)
    room.table = table
    root.mainloop()
