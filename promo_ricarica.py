import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter.messagebox as messagebox
import traceback

class PromoRicaricaApp:
    def __init__(self, master):
        self.master = master
        master.title("Promo Ricarica")
        master.attributes('-fullscreen', True)
        master.update_idletasks()
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        master.geometry(f"{self.width}x{self.height}+0+0")     
        master.config(bg='lightgray')
        master.bind('<Escape>', self.toggle_fullscreen)
        
        self.left_frame = None 
        self.ricarica_values = ["0" for _ in range(10)]
        self.current_ricarica_index = 0

        self.attivazione_var = tk.StringVar(value="disattivato")
        self.tipo_promo_var = tk.StringVar(value="ricarica")
        self.tempo_var = tk.BooleanVar()
        
        self.percentuale_entry = tk.StringVar(value="13")
        self.ora_da = tk.StringVar(value="00:00")
        self.ora_a = tk.StringVar(value="23:59")

        self.current_focus = None
        self.ricarica_labels = []
        self.ricarica_value_labels = []

        self.create_widgets()
        self.leggi_parametri_salvati()

    def create_ricarica_values_column(self, parent):
        ricarica_frame = ttk.Frame(parent)
        ricarica_frame.place(x=50, y=350, width=100, height=300)

        for i, valore in enumerate([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]):
            frame_coppia = ttk.Frame(ricarica_frame)
            frame_coppia.pack(fill=tk.X, pady=2)

            etichetta = ttk.Label(
                frame_coppia, 
                text=str(valore),
                style='Medium.TLabel'
            )
            etichetta.pack(side=tk.LEFT, padx=(0, 10))
            self.ricarica_labels.append(etichetta)

            frame_valore = ttk.Frame(
                frame_coppia,
                style='Valore.TFrame',
                width=100,
                height=25
            )
            frame_valore.pack(side=tk.LEFT)

            etichetta_valore = ttk.Label(
                frame_valore,
                text=self.ricarica_values[i],
                style='Valore.TLabel'
            )
            etichetta_valore.pack()
            self.ricarica_value_labels.append(etichetta_valore)

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, style='TFrame')
        main_frame.place(x=0, y=0, width=self.width, height=self.height)

        left_frame = ttk.Frame(main_frame)
        left_frame.place(x=10, y=10, width=self.width*0.45, height=self.height-20)

        right_frame = ttk.Frame(main_frame)
        right_frame.place(x=self.width*0.45+20, y=10, width=self.width*0.55-30, height=self.height-20)

        y_offset = 10
        self.disattivato_button = ttk.Radiobutton(left_frame, text="DISATTIVATO", variable=self.attivazione_var, value="disattivato", style='Large.TRadiobutton', command=self.update_attivazione)
        self.disattivato_button.place(x=5, y=y_offset, height=20)
        y_offset += 30
        self.attiva_button = ttk.Radiobutton(left_frame, text="ATTIVA", variable=self.attivazione_var, value="attiva", style='Large.TRadiobutton', command=self.update_attivazione)
        self.attiva_button.place(x=5, y=y_offset, height=20)
        y_offset += 30
        ttk.Checkbutton(left_frame, text="TEMPO", variable=self.tempo_var, style='Large.TCheckbutton').place(x=5, y=y_offset, height=20)
        y_offset += 30

        self.a_ricarica_button = ttk.Radiobutton(left_frame, text="A RICARICA", variable=self.tipo_promo_var, value="ricarica", style='Large.TRadiobutton', command=self.update_tipo_promo)
        self.a_ricarica_button.place(x=5, y=y_offset, height=20)
        y_offset += 30
        self.percentuale_button = ttk.Radiobutton(left_frame, text="PERCENTUALE", variable=self.tipo_promo_var, value="percentuale", style='Large.TRadiobutton', command=self.update_tipo_promo)
        self.percentuale_button.place(x=5, y=y_offset, height=20)
        y_offset += 30

        self.create_ricarica_values_column(left_frame)
        ttk.Label(left_frame, text="DA:", style='Large.TLabel').place(x=10, y=y_offset, height=40)
        self.cal_da = DateEntry(left_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', font=('Arial', 14))
        self.cal_da.place(x=60, y=y_offset, height=40)
        self.entry_ora_da = ttk.Entry(left_frame, textvariable=self.ora_da, width=8, font=('Arial', 14))
        self.entry_ora_da.place(x=260, y=y_offset, height=40)
        y_offset += 50

        ttk.Label(left_frame, text="A:", style='Large.TLabel').place(x=10, y=y_offset, height=40)
        self.cal_a = DateEntry(left_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', font=('Arial', 14))
        self.cal_a.place(x=60, y=y_offset, height=40)
        self.entry_ora_a = ttk.Entry(left_frame, textvariable=self.ora_a, width=8, font=('Arial', 14))
        self.entry_ora_a.place(x=260, y=y_offset, height=40)
        y_offset += 50

        self.entry_percentuale = ttk.Entry(left_frame, textvariable=self.percentuale_entry, width=5, font=('Arial', 12))
        self.entry_percentuale.place(x=180, y=y_offset, height=40)
        ttk.Label(left_frame, text="%", style='Large.TLabel').place(x=250, y=y_offset, height=40)
        y_offset += 50

        ttk.Label(left_frame, text="Ricarica €:", style='Large.TLabel').place(x=10, y=300, height=40)
        self.ricarica_label = ttk.Label(left_frame, text="5", style='XLarge.TLabel')
        self.ricarica_label.place(x=130, y=300, height=40)
        self.ricarica_entry = ttk.Entry(left_frame, width=8, font=('Arial', 14))
        self.ricarica_entry.place(x=190, y=300, height=40)
        ttk.Button(left_frame, text="<", command=self.previous_ricarica, width=3, style='Medium.TButton').place(x=280, y=300, height=40)
        ttk.Button(left_frame, text=">", command=self.next_ricarica, width=3, style='Medium.TButton').place(x=330, y=300, height=40)

        self.create_numeric_keypad(right_frame)

        ttk.Button(main_frame, text="Salva", command=self.salva, width=15, style='Large.TButton').place(x=10, y=self.height-100, height=80)
        ttk.Button(main_frame, text="Chiudi", command=self.chiudi, width=15, style='Large.TButton').place(x=250, y=self.height-100, height=80)

        self.entry_ora_da.bind("<FocusIn>", self.set_focus)
        self.entry_ora_a.bind("<FocusIn>", self.set_focus)
        self.entry_percentuale.bind("<FocusIn>", self.set_focus)
        self.ricarica_entry.bind("<FocusIn>", self.set_focus)

        self.left_frame = left_frame

    def create_numeric_keypad(self, parent):
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', ':', 'C'
        ]

        button_width = parent.winfo_width() // 3
        button_height = parent.winfo_height() // 4

        for i, button in enumerate(buttons):
            row, col = divmod(i, 3)
            cmd = lambda x=button: self.numeric_button_click(x)
            ttk.Button(parent, text=button, command=cmd, style='XLarge.TButton').place(
                x=col*button_width + 5, y=row*button_height + 5, 
                width=button_width - 10, height=button_height - 10
            )

    def numeric_button_click(self, value):
        if self.current_focus:
            if value == 'C':
                self.current_focus.delete(0, tk.END)
            else:
                self.current_focus.insert(tk.END, value)

    def set_focus(self, event):
        self.current_focus = event.widget

    def toggle_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))

    def previous_ricarica(self):
        self.save_current_ricarica()
        self.current_ricarica_index = (self.current_ricarica_index - 1) % 10
        self.update_ricarica_display()

    def next_ricarica(self):
        self.save_current_ricarica()
        self.current_ricarica_index = (self.current_ricarica_index + 1) % 10
        self.update_ricarica_display()

    def save_current_ricarica(self):
        value = self.ricarica_entry.get().strip()
        self.ricarica_values[self.current_ricarica_index] = value if value else "0"

    def update_ricarica_display(self):
        valori_ricarica = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        valore_corrente = valori_ricarica[self.current_ricarica_index]
        self.ricarica_label.config(text=str(valore_corrente))
        self.ricarica_entry.delete(0, tk.END)
        self.ricarica_entry.insert(0, self.ricarica_values[self.current_ricarica_index])

        for i, (etichetta, etichetta_valore) in enumerate(zip(self.ricarica_labels, self.ricarica_value_labels)):
            if valori_ricarica[i] == valore_corrente:
                etichetta.configure(style='HighlightedMedium.TLabel')
            else:
                etichetta.configure(style='Medium.TLabel')
            etichetta_valore.config(text=self.ricarica_values[i])

    def update_attivazione(self):
        pass  # Non è più necessario gestire manualmente l'esclusione reciproca

    def update_tipo_promo(self):
        pass  # Non è più necessario gestire manualmente l'esclusione reciproca

    def salva(self):
        self.save_current_ricarica()
        self.salva_promo_tempo()
        self.salva_promo_attivo()

    def salva_promo_tempo(self):
        file_path = os.path.expanduser('~/promo_tempo.csv')
        funzione_globale = "no" if self.attivazione_var.get() == "disattivato" else "si"
        tempo_attivo = "si" if self.tempo_var.get() else "no"
        data_ini = self.cal_da.get_date().strftime("%d/%m/%Y")
        ora_ini = self.ora_da.get()
        data_fine = self.cal_a.get_date().strftime("%d/%m/%Y")
        ora_fine = self.ora_a.get()

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['funzione globale', 'tempo attivo', 'dataini', 'oraini', 'datafine', 'orafine'])
                writer.writerow([funzione_globale, tempo_attivo, data_ini, ora_ini, data_fine, ora_fine])
            print(f"File promo_tempo.csv salvato correttamente")
        except Exception as e:
            print(f"Errore nel salvataggio del file promo_tempo.csv: {str(e)}")
            messagebox.showerror("Errore", f"Errore nel salvataggio del file promo_tempo.csv: {str(e)}")

    def salva_promo_attivo(self):
        file_path = os.path.expanduser('~/promo_attivo.csv')
        funzione_globale = "no" if self.attivazione_var.get() == "disattivato" else "si"
        promo_attiva = "si" if self.attivazione_var.get() == "attiva" else "no"
        percent_attiva = "si" if self.tipo_promo_var.get() == "percentuale" else "no"
        ricarica_attiva = "si" if self.tipo_promo_var.get() == "ricarica" else "no"
        percentuale = self.percentuale_entry.get()

        data = [funzione_globale, promo_attiva, percent_attiva, percentuale, ricarica_attiva] + self.ricarica_values

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['funzione globale', 'promo attiva', 'percent attiva', 'percentuale', 'ricarica attiva', 
                                 '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'])
                writer.writerow(data)
            print(f"File promo_attivo.csv salvato correttamente")
            print(f"Dati salvati: {data}")
        except Exception as e:
            print(f"Errore nel salvataggio del file promo_attivo.csv: {str(e)}")
            messagebox.showerror("Errore", f"Errore nel salvataggio del file promo_attivo.csv: {str(e)}")

    def leggi_parametri_salvati(self):
        self.leggi_promo_tempo()
        self.leggi_promo_attivo()

    def leggi_promo_tempo(self):
        file_path = os.path.expanduser('~/promo_tempo.csv')
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Salta l'intestazione
                row = next(reader, None)
                if row:
                    self.attivazione_var.set("attiva" if row[0] == 'si' else "disattivato")
                    self.tempo_var.set(row[1] == 'si')
                    self.cal_da.set_date(datetime.strptime(row[2], "%d/%m/%Y"))
                    self.ora_da.set(row[3])
                    self.cal_a.set_date(datetime.strptime(row[4], "%d/%m/%Y"))
                    self.ora_a.set(row[5])
        except FileNotFoundError:
            print("File promo_tempo.csv non trovato")
        except Exception as e:
            print(f"Errore lettura parametri tempo: {str(e)}")

    def leggi_promo_attivo(self):
        file_path = os.path.expanduser('~/promo_attivo.csv')
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Salta l'intestazione
                row = next(reader, None)
                if row:
                    print(f"Row letto da promo_attivo.csv: {row}")
                    self.attivazione_var.set("attiva" if row[1] == 'si' else "disattivato")
                    self.tipo_promo_var.set("percentuale" if row[2] == 'si' else "ricarica")
                    self.percentuale_entry.set(row[3])
                    self.ricarica_values = row[5:]
                    self.update_ricarica_display()
        except FileNotFoundError:
            print("File promo_attivo.csv non trovato")
        except Exception as e:
            print(f"Errore lettura parametri attivo: {str(e)}")

    def chiudi(self):
        print("Applicazione in chiusura")
        self.master.quit()

def main():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("Ricarica")
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('Valore.TFrame', background='white', relief='solid')
    style.configure('Valore.TLabel', background='white', font=('Helvetica', 12))
    style.configure('TButton', font=('Arial', 14))
    style.configure('Medium.TButton', font=('Arial', 16))
    style.configure('Large.TButton', font=('Arial', 18))
    style.configure('XLarge.TButton', font=('Arial', 22))
    style.configure('TRadiobutton', font=('Arial', 10))
    style.configure('Large.TRadiobutton', font=('Arial', 12))
    style.configure('TCheckbutton', font=('Arial', 10))
    style.configure('Large.TCheckbutton', font=('Arial', 12))
    style.configure('TLabel', font=('Arial', 14))
    style.configure('Large.TLabel', font=('Arial', 16))
    style.configure('XLarge.TLabel', font=('Arial', 18))
    style.configure('TEntry', font=('Arial', 14))
    style.configure('HighlightedMedium.TLabel', font=('Arial', 16), background='yellow')
    app = PromoRicaricaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.chiudi)
    root.mainloop()

if __name__ == "__main__":
    main()