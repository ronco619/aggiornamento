import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import csv
import threading
import shutil
import subprocess
import zipfile
from datetime import datetime

class AggiornaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema di Aggiornamento")
        self.geometry("1024x800")
        self.configure(bg="white")
        
        # ... (il resto del codice __init__ rimane invariato)

        self.restart_button = tk.Button(self, text="Riavvia Ora", command=self.restart_application, font=("Arial", 12))
        self.restart_button.pack_forget()  # Nascondi inizialmente il pulsante di riavvio

    # ... (le altre funzioni rimangono invariate)

    def apply_updates_and_restart(self):
        self.status_label.config(text="Creazione backup in corso...")
        self.highlight_step(1)
        backup_file = self.create_backup()
        if not backup_file:
            self.status_label.config(text="Errore durante la creazione del backup. Aggiornamento annullato.")
            return

        self.status_label.config(text="Applicazione degli aggiornamenti in corso...")
        self.highlight_step(2)
        try:
            if os.path.exists(self.self_path):
                shutil.rmtree(self.self_path)
            shutil.move(self.download_path, self.self_path)
            os.makedirs(self.download_path)
            self.status_label.config(text="Aggiornamenti applicati. Ripristino backup in corso...")
            
            self.highlight_step(3)
            self.restore_backup(backup_file)
            
            self.status_label.config(text="Aggiornamenti applicati e backup ripristinato con successo.")
            self.highlight_step(4)
            self.update_button.pack_forget()
            self.display_current_version()
            self.show_completion_message()
        except Exception as e:
            self.status_label.config(text=f"Errore durante l'applicazione degli aggiornamenti: {str(e)}")
            os.makedirs(self.download_path)

    def show_completion_message(self):
        self.status_label.config(text="Aggiornamento completato con successo! Premi 'Riavvia Ora' per applicare le modifiche.", fg="green")
        self.restart_button.pack(pady=20)  # Mostra il pulsante di riavvio
        for label in self.step_labels:
            label.config(bg="lightgreen")  # Colora tutti i passaggi in verde chiaro

    def restart_application(self):
        self.save_settings()
        self.destroy()
        subprocess.Popen(["bash", os.path.expanduser("~/restart_self.sh")])

    # ... (il resto del codice rimane invariato)

if __name__ == "__main__":
    app = AggiornaApp()
    app.mainloop()
