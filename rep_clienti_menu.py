import sys
import csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
class VirtualKeyboard(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tastiera Virtuale")
        
        # Ottieni le dimensioni dello schermo
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Imposta la larghezza e l'altezza della finestra
        window_width = 1024
        window_height = 400
        
        # Calcola la posizione x e y per centrare la finestra orizzontalmente
        # e posizionarla nella parte inferiore dello schermo
        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 50  # 50 pixel dal fondo dello schermo
        
        # Imposta la geometria della finestra
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.result = ""

        self.entry = tk.Entry(self, font=("Arial", 40, "bold"))
        self.entry.pack(pady=20, padx=20, fill=tk.X)

        self.create_buttons()

    def create_buttons(self):
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '@'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '', '.', ''],
            ['Chiudi tastiera', 'Spazio', 'Cancella', 'Enter']
        ]

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        button_style = {'font': ("Arial", 24, "bold"), 'width': 4, 'height': 2}

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                if key == 'Spazio':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=3, columnspan=3, sticky='nsew', padx=2, pady=2)
                elif key == 'Cancella':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=6, columnspan=2, sticky='nsew', padx=2, pady=2)
                elif key == 'Enter':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=8, columnspan=2, sticky='nsew', padx=2, pady=2)
                elif key == 'Chiudi tastiera':
                    btn = tk.Button(button_frame, text=key, command=self.close_keyboard, **button_style)
                    btn.grid(row=row, column=0, columnspan=3, sticky='nsew', padx=2, pady=2)
                else:
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)

        # Configura le dimensioni delle righe e delle colonne
        for i in range(5):  # 5 righe
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(10):  # 10 colonne
            button_frame.grid_columnconfigure(i, weight=1)

    def button_click(self, key):
        if key == 'Enter':
            self.result = self.entry.get()
            self.destroy()
        elif key == 'Cancella':
            self.entry.delete(len(self.entry.get())-1, tk.END)
        elif key == 'Spazio':
            self.entry.insert(tk.END, ' ')
        else:
            self.entry.insert(tk.END, key)

    def close_keyboard(self):
        self.result = self.entry.get()
        self.destroy()
        #super().__init__(parent)
        self.title("Tastiera Virtuale")
        
        # Ottieni le dimensioni dello schermo
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Imposta la larghezza e l'altezza della finestra
        window_width = 1024
        window_height = 400
        
        # Calcola la posizione x e y per centrare la finestra orizzontalmente
        # e posizionarla nella parte inferiore dello schermo
        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 50  # 50 pixel dal fondo dello schermo
        
        # Imposta la geometria della finestra
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.result = ""

        self.entry = tk.Entry(self, font=("Arial", 40, "bold"))
        self.entry.pack(pady=20, padx=20, fill=tk.X)

        self.create_buttons()

    def create_buttons(self):
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '@'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', ''],
            ['Chiudi tastiera', 'Spazio', 'Cancella', 'Enter']
        ]

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        button_style = {'font': ("Arial", 24, "bold"), 'width': 4, 'height': 2}

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                if key == 'Spazio':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=3, columnspan=3, sticky='nsew', padx=2, pady=2)
                elif key == 'Cancella':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=6, columnspan=2, sticky='nsew', padx=2, pady=2)
                elif key == 'Enter':
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=8, columnspan=2, sticky='nsew', padx=2, pady=2)
                elif key == 'Chiudi tastiera':
                    btn = tk.Button(button_frame, text=key, command=self.close_keyboard, **button_style)
                    btn.grid(row=row, column=0, columnspan=3, sticky='nsew', padx=2, pady=2)
                else:
                    btn = tk.Button(button_frame, text=key, command=lambda x=key: self.button_click(x), **button_style)
                    btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)

        # Configura le dimensioni delle righe e delle colonne
        for i in range(5):  # 5 righe
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(10):  # 10 colonne
            button_frame.grid_columnconfigure(i, weight=1)

    def button_click(self, key):
        if key == 'Enter':
            self.result = self.entry.get()
            self.destroy()
        elif key == 'Cancella':
            self.entry.delete(len(self.entry.get())-1, tk.END)
        elif key == 'Spazio':
            self.entry.insert(tk.END, ' ')
        else:
            self.entry.insert(tk.END, key)

    def close_keyboard(self):
        self.result = self.entry.get()
        self.destroy()

class ClientiWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestione Clienti")
        self.geometry("1024x800")
        self.attributes('-fullscreen', True)

        # Barra di ricerca
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        self.search_input = tk.Entry(search_frame, width=50, font=('Arial', 24))
        self.search_input.pack(side=tk.LEFT, padx=5)
        self.search_input.bind("<Button-1>", self.open_virtual_keyboard)
        search_button = tk.Button(search_frame, text="Cerca", command=self.filter_table, font=('Arial', 14))
        search_button.pack(side=tk.LEFT)

        # Tabella
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#f0f0f0",
                        fieldbackground="#f0f0f0",
                        rowheight=30,
                        font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
        style.map('Treeview', background=[('selected', '#ADD8E6')])  # Azzurro chiaro per la selezione

        self.table = ttk.Treeview(self, columns=("nome", "cognome", "uid", "euro"), show="headings")
        self.table.heading("nome", text="nome")
        self.table.heading("cognome", text="cognome")
        self.table.heading("uid", text="uid")
        self.table.heading("euro", text="euro")
        
        # Imposta le colonne grigie e la colonna Euro bianca
        self.table.tag_configure('gray', background='#E0E0E0')
        self.table.tag_configure('white', background='white')
        
        self.table.pack(expand=True, fill=tk.BOTH)
        self.table.bind("<Double-1>", self.on_cell_double_clicked)

        # Aggiungi linee orizzontali
        style.configure("Treeview", rowheight=30)
        self.table.tag_configure('evenrow', background='#f0f0f0')
        self.table.tag_configure('oddrow', background='#e9e9e9')

        self.load_data()

        # Pulsanti
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20, fill=tk.X)

        button_style = {'font': ('Arial', 16), 'width': 15, 'height': 2, 'padx': 10, 'pady': 10}

        save_button = tk.Button(button_frame, text="Salva", command=self.save_data, **button_style)
        save_button.pack(side=tk.LEFT, padx=10, expand=True)

        delete_button = tk.Button(button_frame, text="Elimina Cliente", command=self.delete_client, **button_style)
        delete_button.pack(side=tk.LEFT, padx=10, expand=True)

        close_button = tk.Button(button_frame, text="Chiudi", command=self.destroy, **button_style)
        close_button.pack(side=tk.LEFT, padx=10, expand=True)
        

    def load_data(self):
        try:
            with open('/home/self/clienti.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for i, row in enumerate(reader):
                    item = self.table.insert("", tk.END, values=row)
                    self.table.item(item, tags=('gray', 'gray', 'gray', 'white'))
                    if i % 2 == 0:
                        self.table.item(item, tags=('evenrow',))
                    else:
                        self.table.item(item, tags=('oddrow',))
        except FileNotFoundError:
            messagebox.showerror("Errore", "File clienti.csv non trovato.")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante il caricamento dei dati: {str(e)}")

    def on_cell_double_clicked(self, event):
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Informazione", "Nessun elemento selezionato")
            return

        item = selection[0]
        column = self.table.identify_column(event.x)
    
        if column == '#4':  # Euro column
            current_values = self.table.item(item, "values")
            if len(current_values) < 4:
                messagebox.showerror("Errore", "Dati non validi per questa riga")
                return

            current_value = current_values[3]
            keyboard = VirtualKeyboard(self)
            keyboard.entry.insert(0, current_value)
            self.wait_window(keyboard)

            if keyboard.result:
                try:
                    new_value = float(keyboard.result)
                    values = list(current_values)
                    values[3] = f"{new_value:.2f}"
                    self.table.item(item, values=values)
                except ValueError:
                    messagebox.showerror("Errore", "Inserisci un valore numerico valido per Euro.")

    def save_data(self):
        if messagebox.askyesno("Conferma", "Sei sicuro di voler salvare le modifiche?"):
            try:
                with open('/home/self/clienti.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["nome", "cognome", "uid", "euro", "data"])
                    for child in self.table.get_children():
                        writer.writerow(self.table.item(child)["values"])
                messagebox.showinfo("Salvataggio", "Dati salvati con successo!")
            except Exception as e:
                messagebox.showerror("Errore", f"Si è verificato un errore durante il salvataggio: {str(e)}")

    def filter_table(self):
        search_text = self.search_input.get().lower()
        for item in self.table.get_children():
            values = self.table.item(item)["values"]
            nome = str(values[0]).lower()
            cognome = str(values[1]).lower()
            if search_text in nome or search_text in cognome:
                self.table.item(item, tags=())
            else:
                self.table.item(item, tags=("hidden",))
        self.table.tag_configure("hidden", foreground="gray")

    def delete_client(self):
        selected_item = self.table.selection()
        if selected_item:
            item = selected_item[0]
            values = self.table.item(item)["values"]
            if len(values) >= 2:
                nome, cognome = values[:2]
                if messagebox.askyesno("Conferma eliminazione", f"Sei sicuro di voler eliminare il cliente {nome} {cognome}?"):
                    self.table.delete(item)
                    self.save_data()  # Salva i dati dopo l'eliminazione
                    messagebox.showinfo("Eliminazione", "Cliente eliminato con successo!")
            else:
                messagebox.showwarning("Errore", "Dati del cliente non validi.")
        else:
                messagebox.showwarning("Errore", "Seleziona un cliente da eliminare.")

    def open_virtual_keyboard(self, event):
        keyboard = VirtualKeyboard(self)
        keyboard.entry.insert(0, self.search_input.get())
        self.wait_window(keyboard)
        if keyboard.result:
            self.search_input.delete(0, tk.END)
            self.search_input.insert(0, keyboard.result)
            self.filter_table()

if __name__ == '__main__':
    app = ClientiWindow()
    app.mainloop()