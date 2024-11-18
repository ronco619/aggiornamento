import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
from datetime import datetime

# Percorsi dei file da includere nel backup
FILES_TO_BACKUP = [
    "/home/self/clienti.csv",
    "/home/self/credito.csv",
    "/home/self/config_scontrino.csv",
    "/home/self/transactions.csv",
    "/home/self/config_stampante.csv",
    "/home/self/premi.csv",
    "/home/self/timer_settings.json",
    "/home/self/promo_tempo.csv",
    "/home/self/promo_attivo.csv",
    "/home/self/promo_ricarica.csv",
    "/home/self/timer_config.json",
    "/home/self/window_state.json"
]

# Funzione per creare il backup
def crea_backup():
    backup_dir = "/home/self/Desktop/BCK-MANUALE"
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")
    filepath = os.path.join(backup_dir, f"backup_{timestamp}.zip")
    try:
        with zipfile.ZipFile(filepath, 'w') as backup_zip:
            for file in FILES_TO_BACKUP:
                if os.path.exists(file):
                    backup_zip.write(file, os.path.basename(file))
        messagebox.showinfo("Backup", f"Backup creato con successo: {filepath}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la creazione del backup: {str(e)}")

# Funzione per recuperare il backup
def recupera_backup():
    backup_dir = "/home/self/Desktop/BCK-MANUALE"
    filepath = filedialog.askopenfilename(initialdir=backup_dir, filetypes=[("Zip files", "*.zip")])
    if not filepath:
        messagebox.showerror("Errore", "Nessun file selezionato.")
        return
    try:
        with zipfile.ZipFile(filepath, 'r') as backup_zip:
            backup_zip.extractall("/home/self/")
        messagebox.showinfo("Recupero", f"Backup recuperato con successo: {filepath}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il recupero del backup: {str(e)}")

# Funzione per chiudere l'applicazione
def esci():
    root.destroy()

# Configurazione della finestra principale
root = tk.Tk()
root.title("Gestione Backup")
root.attributes('-fullscreen', True)  # Apri in modalità fullscreen
root.geometry("1024x800")

# Creazione dei pulsanti
btn_crea_backup = tk.Button(root, text="Crea Backup", command=crea_backup, width=20, height=2)
btn_crea_backup.pack(pady=20)

btn_recupera_backup = tk.Button(root, text="Recupera da Backup", command=recupera_backup, width=20, height=2)
btn_recupera_backup.pack(pady=20)

btn_esci = tk.Button(root, text="Esci", command=esci, width=20, height=2)
btn_esci.pack(pady=20)

# Avvio dell'applicazione
root.mainloop()