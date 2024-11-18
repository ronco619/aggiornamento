import tkinter as tk
from tkinter import ttk
import os
import csv
from decimal import Decimal, ROUND_DOWN

class CurrencyInput:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        
        # Set window title
        self.root.title("Inserimento Credito")
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Currency entry
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.amount_var,
            font=('Arial', 24),
            justify='right'
        )
        self.amount_entry.pack(fill=tk.X, pady=20)
        
        # Numeric keypad frame
        keypad_frame = ttk.Frame(self.main_frame)
        keypad_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create numeric keypad
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', ',', 'C'
        ]
        
        row = 0
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.press_button(x)
            btn = tk.Button(
                keypad_frame,
                text=button,
                command=cmd,
                font=('Arial', 20),
                width=5,
                height=2
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid weights for keypad
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            keypad_frame.grid_columnconfigure(i, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="Salva",
            command=self.save_amount,
            font=('Arial', 20),
            height=2
        )
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Chiudi",
            command=self.root.quit,
            font=('Arial', 20),
            height=2
        )
        close_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Load existing value if file exists
        self.load_existing_value()
        
    def press_button(self, value):
        if value == 'C':
            self.amount_var.set('')
        else:
            current = self.amount_var.get()
            if value == ',' and ',' in current:
                return
            self.amount_var.set(current + value)
    
    def format_amount(self, amount_str):
        try:
            # Replace comma with dot for decimal parsing
            amount_str = amount_str.replace(',', '.')
            # Convert to Decimal and round to 2 decimal places
            amount = Decimal(amount_str).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            # Convert back to string with comma as decimal separator
            return str(amount).replace('.', ',')
        except:
            return '0,00'
    
    def save_amount(self):
        amount = self.format_amount(self.amount_var.get())
        file_path = os.path.expanduser('~/credito.csv')
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['credito'])
            writer.writerow([amount])
        
        self.root.quit()
    
    def load_existing_value(self):
        file_path = os.path.expanduser('~/credito.csv')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    next(reader)  # Salta l'intestazione
                    value = next(reader)[0]
                    self.amount_var.set(value)
            except:
                self.amount_var.set('0,00')
        else:
            self.amount_var.set('0,00')

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyInput(root)
    root.mainloop()
