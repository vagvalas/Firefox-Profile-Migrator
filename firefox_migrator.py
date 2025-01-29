import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FirefoxMigratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firefox Profile Migrator")
        self.root.geometry("700x800") 
        
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        
        self.categories = {
            "Bookmarks, Downloads and Browsing History": ["places.sqlite", "bookmarkbackups", "favicons.sqlite"],
            "Passwords": ["key4.db", "logins.json"],
            "Site-specific preferences": ["permissions.sqlite", "content-prefs.sqlite"],
            "Search engines": ["search.json.mozlz4"],
            "Personal dictionary": ["persdict.dat"],
            "Autocomplete history": ["formhistory.sqlite"],
            "Cookies": ["cookies.sqlite"],
            "DOM storage": ["webappsstore.sqlite", "chromeappsstore.sqlite"],
            "Extensions": ["extensions"],
            "Security certificate settings": ["cert9.db"],
            "Security device settings": ["pkcs11.txt"],
            "Download actions": ["handlers.json"],
            "Stored session": ["sessionstore.jsonlz4"],
            "Window positions and dialog settings": ["xulstore.json"],
            "User preferences": ["prefs.js"],
            "Containers": ["containers.json"]
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5, fill=tk.X)
        
        self.select_source_button = tk.Button(top_frame, text="Select Source", command=self.select_source)
        self.select_source_button.grid(row=0, column=0, padx=5)
        tk.Label(top_frame, textvariable=self.source_path, wraplength=300).grid(row=0, column=1, padx=5)
        
        self.select_destination_button = tk.Button(top_frame, text="Select Destination", command=self.select_destination, state=tk.DISABLED)
        self.select_destination_button.grid(row=1, column=0, padx=5)
        tk.Label(top_frame, textvariable=self.dest_path, wraplength=300).grid(row=1, column=1, padx=5)
        
        self.go_button = tk.Button(top_frame, text="Go", command=self.migrate, state=tk.DISABLED)
        self.go_button.grid(row=1, column=2, padx=5)
        
        frame_container = tk.Frame(self.root)
        frame_container.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.category_vars = {}
        self.file_vars = {}
        self.file_checkboxes = {}
        self.category_checkboxes = {}
        
        for category, files in self.categories.items():
            cat_var = tk.BooleanVar()
            cat_cb = tk.Checkbutton(frame_container, text=category, variable=cat_var, command=lambda c=category: self.toggle_category(c), state=tk.DISABLED)
            cat_cb.pack(anchor='w', pady=(5, 0))
            self.category_vars[category] = cat_var
            self.category_checkboxes[category] = cat_cb
            
            if len(files) > 1:
                frame_inner = tk.Frame(frame_container)
                frame_inner.pack(anchor='w', padx=20)
                for file in files:
                    var = tk.BooleanVar()
                    cb = tk.Checkbutton(frame_inner, text=file, variable=var, command=lambda c=category: self.update_category(c), state=tk.DISABLED)
                    cb.pack(anchor='w')
                    self.file_checkboxes[file] = cb
                    self.file_vars[file] = var
            else:
                self.file_vars[files[0]] = cat_var  # Directly link single file to category
                self.file_checkboxes[files[0]] = cat_cb
    
    def select_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_path.set(folder)
            self.scan_source()
            self.select_destination_button.config(state=tk.NORMAL)
    
    def select_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_path.set(folder)
            self.enable_go_button()
    
    def scan_source(self):
        source = self.source_path.get()
        if not source:
            return
        
        for category, files in self.categories.items():
            enabled = False
            for file in files:
                if file in self.file_checkboxes:
                    path = os.path.join(source, file)
                    if os.path.exists(path):
                        self.file_checkboxes[file].config(state=tk.NORMAL)
                        enabled = True
                    else:
                        self.file_checkboxes[file].config(state=tk.DISABLED)
                        self.file_vars[file].set(False)
            
            if category in self.category_vars:
                self.category_vars[category].set(False)
                self.category_checkboxes[category].config(state=tk.NORMAL if enabled else tk.DISABLED)
        
        self.enable_go_button()
    
    def enable_go_button(self):
        if self.source_path.get() and self.dest_path.get():
            self.go_button.config(state=tk.NORMAL)
    
    def toggle_category(self, category):
        state = self.category_vars[category].get()
        for file in self.categories[category]:
            if file in self.file_checkboxes and self.file_checkboxes[file].cget('state') == tk.NORMAL:
                self.file_vars[file].set(state)
    
    def update_category(self, category):
        checked_count = sum(self.file_vars[file].get() for file in self.categories[category] if file in self.file_checkboxes and self.file_checkboxes[file].cget('state') == tk.NORMAL)
        total_count = len([file for file in self.categories[category] if file in self.file_checkboxes and self.file_checkboxes[file].cget('state') == tk.NORMAL])
        self.category_vars[category].set(checked_count == total_count)
    
    def migrate(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders")
            return
        
        for file, var in self.file_vars.items():
            if var.get():
                src_file = os.path.join(source, file)
                dest_file = os.path.join(dest, file)
                try:
                    if os.path.isdir(src_file):
                        shutil.copytree(src_file, dest_file, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src_file, dest_file)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy {file}: {str(e)}")
                    return
        
        messagebox.showinfo("Success", "Migration completed successfully!")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FirefoxMigratorApp(root)
    root.mainloop()