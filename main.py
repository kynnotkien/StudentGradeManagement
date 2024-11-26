# Made by KynNotKien <3
# ------------------------------------------------------------------------------------------------
# Importing Libraries
# pip install pandas
# ------------------------------------------------------------------------------------------------
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

# Create the main window

class Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Management System")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)

# UI/UX

class UI(tk.Frame):
    def __init__(self, parent):
        pass
class LoadData:
    def __init__(self):
        self.df = pd.read_csv(FILE_PATH)

# Table create

class Table(tk.Frame):
    def __init__(self, parent, room=None):
        super().__init__(parent)
        self.room = room
        self.pack(fill=tk.X, padx=10, pady=10, side=tk.RIGHT)
        
        # Create a fixed size frame to contain the table
        self.table_frame = tk.Frame(self, width=900, height=500)
        self.table_frame.pack(expand=False)
        self.table_frame.pack_propagate(False)
        
        # Create scrollbars
        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # Configure column widths
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Load data first
        self.df = pd.read_csv(FILE_PATH)
        
        # Create Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=list(self.df.columns), show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.Y)
        
        # Configure columns
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=94, stretch=True, anchor=tk.CENTER)
        
        # Add data to Treeview
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)
    
    def on_select(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]
            # Update each entry with corresponding value
            labels = ['ID:', 'Name:', 'Maths:', 'Science:', 'English:', 
                     'Social:', 'Computer:', 'Average:', 'Grade:']
            for label, value in zip(labels, record):
                if label in self.room.entries:
                    self.room.entries[label].delete(0, tk.END)
                    self.room.entries[label].insert(0, value)
            return record

    def update_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

# Controler, editer, buttons place

class Room(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.entries = {}
        self.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)

        # Set background for the frame
        self.configure(bg=DARK_GREY)
        self.pack_propagate(False)
        self.configure(width=300, height=500)
        
        # Create frames for buttons and edit area
        self.button_frame = Button(self)
        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack(side=tk.TOP, padx=10, fill=tk.X)
        self.edit_frame.configure(bg=DARK_GREY)
        
        # Create entry fields
        labels = ['ID:', 'Name:', 'Maths:', 'Science:', 'English:', 
                 'Social:', 'Computer:', 'Average:', 'Grade:']
        
        for i, label in enumerate(labels):
            tk.Label(self.edit_frame, bg=DARK_GREY, text=label, font=("Helvetica", 10)).grid(row=i, column=0, sticky='w', ipadx=5, padx=5, pady=2)
            entry = tk.Entry(self.edit_frame, width=50, font=("Helvetica", 10))
            entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
            self.entries[label] = entry

        # Create actual button widgets that call the functions
        delete_btn = tk.Button(self.button_frame, text="Delete", command=self.button_frame.delete)
        add_btn = tk.Button(self.button_frame, text="Add", command=self.button_frame.add)
        update_btn = tk.Button(self.button_frame, text="Update", command=self.button_frame.update)
        
        # Pack the actual button widgets
        self.button_frame.pack(side=tk.BOTTOM, padx=10)
        self.button_frame.configure(bg=DARK_GREY)
        delete_btn.pack(side=tk.LEFT, padx=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        update_btn.pack(side=tk.LEFT, padx=5)
class Search(tk.Frame):
    def __init__(self, parent):
        pass

# Button function

class Button(tk.Frame):
    def __init__(self, parent, room=None):
        super().__init__(parent)
        self.room = room  # Store reference to Room instance
    
    def delete(self):
        print("Delete")

    # Add Function
    def add(self):

        # Error Handling
        if self.room.entries['ID:'].get() == "":
            messagebox.showerror("Error", "ID cannot be empty")
            return
        if self.room.entries['Name:'].get() == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if self.room.entries['Maths:'].get() == "":
            messagebox.showerror("Error", "Maths cannot be empty")
            return
        if self.room.entries['Science:'].get() == "":
            messagebox.showerror("Error", "Science cannot be empty")
            return
        if self.room.entries['English:'].get() == "":
            messagebox.showerror("Error", "English cannot be empty")
            return
        if self.room.entries['Social:'].get() == "":
            messagebox.showerror("Error", "Social cannot be empty")
            return
        if self.room.entries['Computer:'].get() == "":
            messagebox.showerror("Error", "Computer cannot be empty")
            return
        else:
            FILE_PATH
            with open(FILE_PATH, "a", newline='') as file:
            # Get values from all entry fields using room reference
                values = []
                for label in ['ID:', 'Name:', 'Maths:', 'Science:', 'English:', 'Social:', 'Computer:', 'Average:', 'Grade:']:
                    values.append(self.room.entries[label].get())
                
                # Write values as comma-separated string
                file.write(",".join(values) + "\n")

    def update(self):
        pass
        # FILE_PATH
        # new_values = []
        # with open(FILE_PATH, "w") as file:
        #     for label in ['ID:', 'Name:', 'Maths:', 'Science:', 'English:', 'Social:', 'Computer:', 'Average:', 'Grade:']:
        #         new_values.append(self.room.entries[label].get())
        #     print(record,new_values)
        #     file.write(",".replace(record, new_values))



class Edit(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        pass

class Exit:
    def __init__(self):
        pass

# Run the application

if __name__ == "__main__":
    root = tk.Tk()
    app = Screen(root)
    ui = UI(root)
    room = Room(root)
    table = Table(root, room)
    load_data = LoadData()
    search = Search(root)
    button = Button(room)
    edit = Edit(root)
    exit = Exit()
    root.mainloop()