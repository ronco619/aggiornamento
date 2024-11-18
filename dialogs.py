import tkinter as tk
from tkinter import ttk
import logging

class TouchFriendlyDialog:
    def __init__(self, parent, title, message):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x300")
        self.top.attributes('-fullscreen', True)

        frame = ttk.Frame(self.top, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=message, wraplength=350, font=('Arial', 14)).pack(pady=20)
        ttk.Button(frame, text="OK", command=self.top.destroy, style='Large.TButton').pack(pady=20)

        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 20, 'bold'), padding=10)

    def show(self):
        self.top.update()
        try:
            self.top.grab_set()
        except tk.TclError:
            logging.warning("Impossibile impostare il grab sulla finestra di dialogo")
        self.top.wait_window()

class TouchFriendlyConfirmDialog:
    def __init__(self, parent, title, message):
        self.result = False
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x300")
        self.top.attributes('-fullscreen', True)

        frame = ttk.Frame(self.top, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=message, wraplength=350, font=('Arial', 14)).pack(pady=20)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Sì", command=self.yes, style='Large.TButton').pack(side="left", padx=10)
        ttk.Button(button_frame, text="No", command=self.no, style='Large.TButton').pack(side="left", padx=10)

    def yes(self):
        self.result = True
        self.top.destroy()

    def no(self):
        self.result = False
        self.top.destroy()

    def show(self):
        self.top.update()
        try:
            self.top.grab_set()
        except tk.TclError:
            logging.warning("Impossibile impostare il grab sulla finestra di conferma")
        self.top.wait_window()
        return self.result