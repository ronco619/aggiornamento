import RPi.GPIO as GPIO
from datetime import datetime
import csv
import os
import tkinter as tk
from tkinter import ttk


class TransactionTracker:
    def __init__(self):
        self.gpio_pin = 17
        self.transactions_file = '/home/self/transactions.csv'
        self.closures_file = '/home/self/chiusure.csv'
        self.is_closed = False
        self.current_closure = None
        self.closures = []
        self.setup_gpio()
        self.setup_gui()
        self.load_closures()

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        try:
            GPIO.add_event_detect(self.gpio_pin, GPIO.BOTH, callback=self.gpio_callback, bouncetime=300)
        except RuntimeError:
            print(f"Impossibile aggiungere il rilevamento dell'evento. Il pin {self.gpio_pin} potrebbe essere in uso.")
            print("Prova a eseguire lo script con privilegi di superutente (sudo).")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.geometry("1024x600")
        self.root.attributes('-fullscreen', True)
        
        self.label = tk.Label(self.root, text="In attesa...", font=("Arial", 24), wraplength=900)
        self.label.pack(expand=True)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, columns=("Numero", "Inizio", "Fine", "Importo"), show="headings")
        self.tree.heading("Numero", text="Numero")
        self.tree.heading("Inizio", text="Inizio")
        self.tree.heading("Fine", text="Fine")
        self.tree.heading("Importo", text="Importo")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.simulate_button = tk.Button(self.root, text="Simula Interruttore", command=self.simulate_switch, font=("Arial", 18))
        self.simulate_button.pack(side=tk.BOTTOM, pady=10)

        self.close_button = tk.Button(self.root, text="Chiudi Programma", command=self.on_closing, font=("Arial", 18))
        self.close_button.pack(side=tk.BOTTOM, pady=10)

    def load_closures(self):
        self.closures = []
        if os.path.exists(self.closures_file):
            with open(self.closures_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.closures.append({
                        'number': int(row[0]),
                        'start_time': datetime.strptime(row[1], '%d/%m/%y %H:%M'),
                        'end_time': datetime.strptime(row[2], '%d/%m/%y %H:%M') if row[2] else None,
                        'amount': float(row[3]) if row[3] else 0
                    })
        self.closures.sort(key=lambda x: x['start_time'], reverse=True)
        if self.closures:
            self.current_closure = self.closures[0]
            if not self.current_closure['end_time']:
                self.is_closed = True
            else:
                self.start_new_closure()
        else:
            self.start_new_closure()
        self.update_display()
        self.update_closure_list()

    def start_new_closure(self):
        if self.closures:
            new_number = self.closures[0]['number'] + 1
        else:
            new_number = 1
        self.current_closure = {
            'number': new_number,
            'start_time': datetime.now().replace(second=0, microsecond=0),
            'end_time': None,
            'amount': 0
        }
        self.is_closed = True
        self.closures.insert(0, self.current_closure)
        self.update_display()
        self.save_closure()

    def end_closure(self):
        if self.current_closure and self.is_closed:
            self.current_closure['end_time'] = datetime.now().replace(second=0, microsecond=0)
            self.current_closure['amount'] = self.calculate_total(self.current_closure['start_time'], self.current_closure['end_time'])
            self.save_closure()
            self.is_closed = False
            self.update_display()
        self.update_closure_list()

    def calculate_total(self, start_date, end_date):
        total = 0
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trans_datetime = datetime.strptime(f"{row['Data']} {row['Ora'][:5]}", '%d/%m/%y %H:%M')
                    if start_date <= trans_datetime <= end_date:
                        total += float(row['Valore'])
        except Exception as e:
            print(f"Errore nel calcolo del totale: {str(e)}")
        return total

    def save_closure(self):
        with open(self.closures_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for closure in self.closures:
                writer.writerow([
                    closure['number'],
                    closure['start_time'].strftime('%d/%m/%y %H:%M'),
                    closure['end_time'].strftime('%d/%m/%y %H:%M') if closure['end_time'] else '',
                    f"{closure['amount']:.2f}"
                ])

    def update_display(self):
        if self.is_closed:
            text = f"CHIUSURA {self.current_closure['number']} {self.current_closure['start_time'].strftime('%d/%m/%y %H:%M')} AL **********************"
        else:
            text = f"CHIUSURA {self.current_closure['number']} {self.current_closure['start_time'].strftime('%d/%m/%y %H:%M')} AL {self.current_closure['end_time'].strftime('%d/%m/%y %H:%M')} € {self.current_closure['amount']:.2f}"
        self.label.config(text=text)
        print(text)

    def update_closure_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for closure in self.closures:
            self.tree.insert("", "end", values=(
                closure['number'],
                closure['start_time'].strftime('%d/%m/%y %H:%M'),
                closure['end_time'].strftime('%d/%m/%y %H:%M') if closure['end_time'] else '**********************',
                f"€ {closure['amount']:.2f}" if closure['end_time'] else '**********************'
            ))

    def simulate_switch(self):
        self.gpio_callback(self.gpio_pin)

    def gpio_callback(self, channel):
        if GPIO.input(channel) == GPIO.LOW or not self.is_closed:
            self.start_new_closure()
        else:
            self.end_closure()

    def on_closing(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gpio_setup = False
    try:
        tracker = TransactionTracker()
        gpio_setup = True
        tracker.run()
    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")
    finally:
        if gpio_setup:
            GPIO.cleanup()