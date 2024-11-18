#virtual_number.py
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

class VirtualNumberKeyboard(tk.Frame):
    def __init__(self, parent, entry, on_enter=None, on_key_press=None):
        tk.Frame.__init__(self, parent)
        self.entry = entry
        self.on_enter_callback = on_enter
        self.on_key_press_callback = on_key_press
        self.create_buttons()

    def create_buttons(self):
        keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', '←']
        ]
        main_keyboard = tk.Frame(self)
        main_keyboard.grid(row=0, column=0, padx=(0, 5))

        button_font = tkfont.Font(family="Arial", size=18, weight="bold")

        for row, key_row in enumerate(keys):
            key_frame = tk.Frame(main_keyboard)
            key_frame.grid(row=row, column=0)
            for col, key in enumerate(key_row):
                if key == '←':
                    button = tk.Button(key_frame, text=key, width=4, height=2,
                                       command=self.backspace,
                                       font=button_font, bg='yellow')
                else:
                    button = tk.Button(key_frame, text=key, width=4, height=2,
                                       command=lambda x=key: self.button_click(x),
                                       font=button_font)
                button.grid(row=0, column=col, padx=2, pady=2)

        enter_button = tk.Button(self, text='Invio\n↵', width=6, height=10,
                                 command=self.on_enter, font=button_font, bg='green', fg='white')
        enter_button.grid(row=0, column=1, rowspan=4, padx=(5, 0), pady=2, sticky='ns')

    def button_click(self, key):
        self.entry.insert(tk.END, key)
        if self.on_key_press_callback:
            self.on_key_press_callback()

    def backspace(self):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_text[:-1])
        if self.on_key_press_callback:
            self.on_key_press_callback()

    def on_enter(self):
        if self.on_enter_callback:
            self.on_enter_callback()
        if self.on_key_press_callback:
            self.on_key_press_callback()

# Esempio di utilizzo
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tastiera Numerica Virtuale")

    entry = tk.Entry(root, font=("Arial", 18))
    entry.pack(pady=10)

    def on_enter():
        print("Invio premuto! Valore:", entry.get())

    keyboard = VirtualNumberKeyboard(root, entry, on_enter=on_enter)
    keyboard.pack(pady=10)

    root.mainloop()