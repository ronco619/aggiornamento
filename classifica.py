import csv
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, StringVar, IntVar
import os
from datetime import datetime, timedelta
import tkinter.font as tkFont
import tkinter as tk


class VirtualNumberKeyboard:
    def __init__(self, parent, entry):
        self.parent = parent
        self.entry = entry
        self.keyboard_frame = tk.Frame(self.parent, bg='lightgray', bd=2, relief='raised')
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', 'C'
        ]
        row = 0
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(self.keyboard_frame, text=button, width=5, height=2, command=cmd).grid(row=row, column=col, padx=1, pady=1)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def click(self, key):
        if key == 'C':
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])
        else:
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current + key)

    def place(self, x, y):
        self.keyboard_frame.place(x=x, y=y)

    def pack(self):
        self.keyboard_frame.pack()

    def destroy(self):
        self.keyboard_frame.destroy()

def print_csv_preview(file_path, num_rows=5):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            print("Intestazioni CSV:", headers)
            print("Prime righe del file:")
            for i, row in enumerate(reader):
                if i < num_rows:
                    print(row)
                else:
                    break
    except Exception as e:
        print(f"Errore nella lettura del file CSV: {e}")

def load_and_process_data(mode='total'):
    totals = defaultdict(float)
    current_date = datetime.now()
    current_month = current_date.replace(day=1)
    last_month_end = current_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    
    def parse_date(date_string):
        formats = ['%d-%m-%Y', '%d/%m/%y', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        raise ValueError(f"Formato data non riconosciuto: {date_string}")

    with open('/home/self/Desktop/SELF/transactions.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Cliente' in row:
                cliente = row['Cliente']
            elif 'nome' in row and 'cognome' in row:
                cliente = f"{row['nome']} {row['cognome']}".strip()
            else:
                print(f"Riga non valida: {row}")
                continue

            if 'Valore' not in row or 'Data' not in row:
                print(f"Dati mancanti per il cliente: {cliente}")
                continue

            valore = row['Valore']
            tipo = row.get('Tipo', '').lower()
            
            try:
                data = parse_date(row['Data'])
            except ValueError as e:
                print(f"Errore nella data per il cliente {cliente}: {e}")
                continue

            if 'ricarica' in tipo:
                try:
                    amount = float(valore.replace(',', '.'))
                    if mode == 'total' or (mode == 'monthly' and last_month_start <= data <= last_month_end):
                        totals[cliente] += amount
                except ValueError:
                    print(f"Errore nel convertire il valore: {valore} per il cliente {cliente}")
    
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return sorted_totals, current_month, last_month_start

def load_prizes():
    prize_file = '/home/self/premi.csv'
    if not os.path.exists(prize_file):
        return []
    with open(prize_file, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader if 'pinvio' in row]

def save_prizes(root, prizes, data, tree, info_label, prize_history_tree, mode_var, current_month, last_month):
    file_path = '/home/self/clienti.csv'
    prize_file = '/home/self/premi.csv'
    
    existing_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = f"{row['nome']} {row['cognome']}"
                existing_data[key] = {
                    'uid': row['uid'],
                    'euro': float(row['euro']),
                    'data': row['data'],
                }

    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    prizes_info = []
    for i, (cliente, total) in enumerate(data[:10]):
        if i < len(prizes) and prizes[i].get():
            prize = float(prizes[i].get())
            if cliente in existing_data:
                existing_data[cliente]['euro'] += prize
                existing_data[cliente]['data'] = current_date
            else:
                nome, cognome = cliente.split(' ', 1) if ' ' in cliente else (cliente, '')
                existing_data[cliente] = {
                    'uid': 'N/A',
                    'euro': total + prize,
                    'data': current_date
                }
            prizes_info.append({'cliente': cliente, 'premio': f"{prize:.2f}", 'data': current_date, 'pinvio': f"{total:.2f}", 'approvato': 'N'})

    with open(file_path, 'w', newline='') as file:
        fieldnames = ['nome', 'cognome', 'uid', 'euro', 'data']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for cliente, info in existing_data.items():
            nome, cognome = cliente.split(' ', 1) if ' ' in cliente else (cliente, '')
            writer.writerow({
                'nome': nome,
                'cognome': cognome,
                'uid': info['uid'],
                'euro': f"{info['euro']:.2f}",
                'data': info['data'],
            })

    existing_prizes = load_prizes()
    all_prizes = existing_prizes + prizes_info
    with open(prize_file, 'w', newline='') as file:
        fieldnames = ['cliente', 'premio', 'data', 'pinvio', 'approvato']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for prize in all_prizes[-10:]:
            if 'approvato' not in prize:
                prize['approvato'] = 'N'
            writer.writerow({
                'cliente': prize['cliente'],
                'premio': f"{float(prize['premio']):.2f}",
                'data': prize['data'],
                'pinvio': f"{float(prize['pinvio']):.2f}",
                'approvato': prize['approvato']
            })

    update_gui(root, tree, data, prizes, info_label, prize_history_tree, mode_var.get(), current_month, last_month)
    
def update_gui(root, tree, data, prizes, info_label, prize_history_tree, mode, current_month, last_month_start):
    for item in tree.get_children():
        tree.delete(item)
    
    if mode == 'monthly':
        month_label.config(text=f"Dati relativi a: {last_month_start.strftime('%B %Y')}")
    else:
        month_label.config(text="Dati totali")

    tree.tag_configure('gold', background='gold')
    tree.tag_configure('silver', background='silver')
    tree.tag_configure('bronze', background='sandybrown')

    for i, (cliente, total) in enumerate(data, start=1):
        if i <= 10 and prizes[i-1].get():
            prize = float(prizes[i-1].get())
            total += prize
        if i == 1:
            tree.insert('', tk.END, values=(f"{i}°", cliente, f"€ {total:.2f}"), tags=('gold',))
        elif i == 2:
            tree.insert('', tk.END, values=(f"{i}°", cliente, f"€ {total:.2f}"), tags=('silver',))
        elif i == 3:
            tree.insert('', tk.END, values=(f"{i}°", cliente, f"€ {total:.2f}"), tags=('bronze',))
        else:
            tree.insert('', tk.END, values=(f"{i}°", cliente, f"€ {total:.2f}"))

    prizes_info = load_prizes()
    if prizes_info:
        info_text = "  ULTIMI 10 PREMI INVIATI "
        last_prize = prizes_info[-1]
        info_label.config(text=f"{info_text}\nUltimo premio: {last_prize['cliente']} - €{float(last_prize['premio']):.2f} - {last_prize['data']}", 
                          background='yellow')
    else:
        info_text = "Nessun premio è stato inviato."
        info_label.config(text=info_text, background='light gray')

    for item in prize_history_tree.get_children():
        prize_history_tree.delete(item)
    for prize in prizes_info[-10:]:
        prize_history_tree.insert('', tk.END, values=(
            prize['cliente'], 
            f"€{float(prize['premio']):.2f}", 
            prize['data'], 
            f"€{float(prize['pinvio']):.2f}"
        ))

    # Aggiorna la larghezza delle colonne del prize_history_tree
    for col in prize_history_tree['columns']:
        prize_history_tree.column(col, width=tkFont.Font().measure(col.title()))
        for item in prize_history_tree.get_children():
            col_value = prize_history_tree.set(item, col)
            col_width = tkFont.Font().measure(col_value)
            if prize_history_tree.column(col, width=None) < col_width:
                prize_history_tree.column(col, width=col_width)

    # Centra il contenuto delle colonne
    for col in prize_history_tree['columns']:
        prize_history_tree.heading(col, anchor='center')
        prize_history_tree.column(col, anchor='center')

    # Aggiorna la GUI
    root.update_idletasks()

def create_gui(data):
    global mode_var, month_label

    root = tk.Tk()
    root.title("classifica")
    root.attributes('-fullscreen', True)
    #config_window.overrideredirect(True)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=1)

    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    tree_frame = ttk.Frame(left_frame)
    tree_frame.pack(fill=tk.BOTH, expand=1)

    tree = ttk.Treeview(tree_frame, columns=('Posizione', 'Cliente', 'Totale'), show='headings')
    tree.heading('Posizione', text='Pos.')
    tree.heading('Cliente', text='Cliente')
    tree.heading('Totale', text='Totale Ricaricato')
    
    tree.column('Posizione', width=50, anchor='center')
    tree.column('Cliente', width=400, anchor='w')
    tree.column('Totale', width=150, anchor='e')

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    style = ttk.Style()
    style.configure("Big.TButton", padding=(20, 10), font=('Helvetica', 12, 'bold'))

    radio_frame = ttk.LabelFrame(left_frame, text="Modalità di visualizzazione", padding="10")
    radio_frame.pack(fill=tk.X, pady=10)

    mode_var = StringVar(value="total")

    ttk.Radiobutton(radio_frame, text="Totale", variable=mode_var, value="total").pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(radio_frame, text="Mensile", variable=mode_var, value="monthly").pack(side=tk.LEFT, padx=10)

    month_label = ttk.Label(radio_frame, text="")
    month_label.pack(side=tk.RIGHT, padx=10)

    prize_keyboard_frame = ttk.Frame(left_frame)
    prize_keyboard_frame.pack(fill=tk.X, pady=10)

    prize_frame = ttk.LabelFrame(prize_keyboard_frame, text="Premi per i primi 10", padding="10")
    prize_frame.pack(side=tk.LEFT, fill=tk.Y)

    keyboard_frame = ttk.Frame(prize_keyboard_frame)
    keyboard_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(10, 0))

    prizes = []
    keyboard_container = [None]

    def show_keyboard(entry):
        if keyboard_container[0]:
            keyboard_container[0].destroy()
        
        x_offset = 170
        y_offset = -4
        
        keyboard_container[0] = VirtualNumberKeyboard(keyboard_frame, entry)
        keyboard_container[0].pack()
        keyboard_container[0].place(x=x_offset, y=y_offset)

    def hide_keyboard(event):
        if keyboard_container[0]:
            keyboard_container[0].destroy()
            keyboard_container[0] = None

    for i in range(10):
        ttk.Label(prize_frame, text=f"{i+1}°").grid(row=i, column=0, padx=5, pady=2)
        prize_entry = ttk.Entry(prize_frame, width=10)
        prize_entry.grid(row=i, column=1, padx=5, pady=2)
        
        prize_entry.bind("<FocusIn>", lambda event, e=prize_entry: show_keyboard(e))
        prize_entry.bind("<FocusOut>", hide_keyboard)
        
        prizes.append(prize_entry)

    info_label = ttk.Label(right_frame, text="", wraplength=400, justify="left")
    info_label.pack(pady=10, fill=tk.X)

    prize_history_frame = ttk.Frame(right_frame)
    prize_history_frame.pack(fill=tk.BOTH, expand=1)

    prize_history_tree = ttk.Treeview(prize_history_frame, columns=('Cliente', 'Premio', 'Data'), show='headings')
    prize_history_tree.heading('Cliente', text='Cliente')
    prize_history_tree.heading('Premio', text='Premio')
    prize_history_tree.heading('Data', text='Data')
    prize_history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    prize_history_scrollbar = ttk.Scrollbar(prize_history_frame, orient=tk.VERTICAL, command=prize_history_tree.yview)
    prize_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    prize_history_tree.configure(yscrollcommand=prize_history_scrollbar.set)

    button_frame = ttk.Frame(left_frame)
    button_frame.pack(fill=tk.X, pady=20)

    save_button = ttk.Button(button_frame, text="Invia premi e salva", 
                             command=lambda: save_prizes(root, prizes, data, tree, info_label, prize_history_tree, mode_var, current_month, last_month),
                             style="Big.TButton")
    save_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

    close_button = ttk.Button(button_frame, text="Chiudi", command=root.quit, style="Big.TButton")
    close_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))



    def update_data():
        nonlocal data
        mode = mode_var.get()
        data, current_month, last_month = load_and_process_data(mode)
        update_gui(root, tree, data, prizes, info_label, prize_history_tree, mode, current_month, last_month)

    mode_var.trace('w', lambda *args: update_data())

    update_gui(root, tree, data, prizes, info_label, prize_history_tree, 'total', current_month, last_month)
    
    def main():
        root = tk.Tk()
        root.attributes('-topmost', True)
        #root.title("classifica")
    root.mainloop()

if __name__ == "__main__":
    try:
        print("Anteprima del file transactions.csv:")
        print_csv_preview('/home/self/Desktop/SELF/transactions.csv')
        
        data, current_month, last_month = load_and_process_data()
        create_gui(data)
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        input("Premi Enter per chiudere...")
        main()