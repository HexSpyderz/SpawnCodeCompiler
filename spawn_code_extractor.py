import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import winsound

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def on_enter(e, button):
    button['background'] = '#3C8DBC'

def on_leave(e, button):
    button['background'] = '#2C3E50'

class App:
    def __init__(self, root):
        self.list_folders = False
        self.include_subfolders = True
        self.output_filename = 'output.txt'

        background_image_path = resource_path("your_image.png")
        self.background_image = tk.PhotoImage(file=background_image_path)
        bg_label = tk.Label(root, image=self.background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {'font': ('Helvetica', 12, 'bold'), 'fg': 'white', 'bg': '#2C3E50', 'activebackground': '#3C8DBC'}

        self.select_button = tk.Button(root, text="Select Resource Folder", command=self.select_folder, **button_style)
        self.select_button.pack(expand=True)

        self.select_button.bind("<Enter>", lambda e: on_enter(e, self.select_button))
        self.select_button.bind("<Leave>", lambda e: on_leave(e, self.select_button))

        self.settings_button = tk.Button(root, text="Settings", command=self.open_settings, **button_style)
        self.settings_button.pack(expand=True)

        self.settings_button.bind("<Enter>", lambda e: on_enter(e, self.settings_button))
        self.settings_button.bind("<Leave>", lambda e: on_leave(e, self.settings_button))

        self.label = tk.Label(root, text="Made by Hex", fg='white')
        self.label.pack(side='bottom', anchor='se')


    def select_folder(self):
        winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.process_files(folder_path)

    def process_files(self, folder_path):
        items = set()
        for root, dirs, files in os.walk(folder_path):
            if not self.include_subfolders and root != folder_path:
                continue
            if self.list_folders:
                items.update(dirs)
            else:
                for file in files:
                    if file.endswith('.yft') and not file.endswith('_hi.yft'):
                        items.add(os.path.splitext(file)[0])
        self.write_to_file(items)

    def write_to_file(self, items):
        with open(self.output_filename, 'w') as file:
            for item in items:
                file.write(f"{item}\n")
        messagebox.showinfo("Complete", f"Operation has been completed. Output saved to {self.output_filename}.")

    def open_settings(self):
        settings_window = Toplevel(root)
        settings_window.title("Settings")

        tk.Checkbutton(settings_window, text="List folder names instead of file names", 
                       variable=tk.BooleanVar(value=self.list_folders), 
                       command=lambda: setattr(self, 'list_folders', not self.list_folders)).pack()

        tk.Checkbutton(settings_window, text="Include subfolders in search", 
                       variable=tk.BooleanVar(value=self.include_subfolders), 
                       command=lambda: setattr(self, 'include_subfolders', not self.include_subfolders)).pack()

        tk.Label(settings_window, text="Output file name:").pack()
        output_name_entry = tk.Entry(settings_window)
        output_name_entry.insert(0, self.output_filename)
        output_name_entry.pack()
        tk.Button(settings_window, text="Save Output File Name", 
                  command=lambda: setattr(self, 'output_filename', output_name_entry.get())).pack()

root = tk.Tk()
root.title("FiveM Resource Processor")
root.geometry("600x400")

app = App(root)

root.mainloop()
