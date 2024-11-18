import tkinter as tk
from tkinter import font

class TouchFriendlyDialog:
    def __init__(self, parent, title, message):
        self.parent = parent
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.attributes('-fullscreen', True)

        large_font = font.Font(family="Helvetica", size=16)

        frame = tk.Frame(self.dialog, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        message_label = tk.Label(frame, text=message, font=large_font, wraplength=360)
        message_label.pack(expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        ok_button = tk.Button(button_frame, text="OK", font=large_font, command=self.on_ok, height=2, width=10)
        ok_button.pack(side=tk.BOTTOM)

    def on_ok(self):
        self.result = True
        self.dialog.destroy()

    def show(self):
        self.dialog.grab_set()
        self.dialog.wait_window()
        return self.result

class TouchFriendlyConfirmDialog(TouchFriendlyDialog):
    def __init__(self, parent, title, message):
        super().__init__(parent, title, message)

        large_font = font.Font(family="Helvetica", size=16)

        button_frame = self.dialog.winfo_children()[0].winfo_children()[-1]
        yes_button = tk.Button(button_frame, text="Sì", font=large_font, command=self.on_yes, height=2, width=10)
        no_button = tk.Button(button_frame, text="No", font=large_font, command=self.on_no, height=2, width=10)

        yes_button.pack(side=tk.LEFT, expand=True, padx=10)
        no_button.pack(side=tk.RIGHT, expand=True, padx=10)

    def on_yes(self):
        self.result = True
        self.dialog.destroy()

    def on_no(self):
        self.result = False
        self.dialog.destroy()