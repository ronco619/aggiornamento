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
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self, text="Premi 'Controlla Aggiornamenti' per iniziare.", bg="white", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.check_button = tk.Button(self, text="Controlla Aggiornamenti", command=self.check_updates, font=("Arial", 12))
        self.check_button.pack(pady=20)
        
        self.update_button = tk.Button(self, text="Aggiorna e Riavvia", command=self.apply_updates_and_restart, font=("Arial", 12))
        self.update_button.pack(pady=20)

        self.version_label = tk.Label(self, text="", bg="white", font=("Arial", 12))
        self.version_label.pack(pady=20)

        self.current_version_label = tk.Label(self, text="", bg="white", font=("Arial", 12))
        self.current_version_label.pack(pady=20)

        self.close_button = tk.Button(self, text="Chiudi", command=self.chiudi_app, font=("Arial", 12))
        self.close_button.pack(pady=20)

        self.restart_button = tk.Button(self, text="Riavvia Ora", command=self.restart_application, font=("Arial", 12))
        self.restart_button.pack_forget()  # Nascondi inizialmente il pulsante di riavvio

        # Lista dei passaggi
        self.steps_frame = tk.Frame(self, bg="white")
        self.steps_frame.pack(pady=20)
        self.steps = [
            "1. Controllo aggiornamenti",
            "2. Creazione backup",
            "3. Applicazione aggiornamenti",
            "4. Ripristino dati",
            "5. Completato"
        ]
        self.step_labels = []
        for step in self.steps:
            label = tk.Label(self.steps_frame, text=step, bg="white", font=("Arial", 12))
            label.pack(anchor="w")
            self.step_labels.append(label)

        self.github_repo = "https://api.github.com/repos/ronco619/aggiornamento/contents/"
        self.download_path = "/home/self/Desktop/AGGIORNAMENTI"
        self.self_path = "/home/self/Desktop/SELF"
        self.backup_dir = "/home/self/Desktop/BCK-MANUALE"

        self.FILES_TO_BACKUP = [
            "/home/self/Desktop/SELF/clienti.csv",
            "/home/self/credito.csv",
            "/home/self/config_scontrino.csv",
            "/home/self/Desktop/SELF/transactions.csv",
            "/home/self/config_stampante.csv",
            "/home/self/premi.csv",
            "/home/self/timer_settings.json",
            "/home/self/promo_tempo.csv",
            "/home/self/promo_attivo.csv",
            "/home/self/promo_ricarica.csv",
            "/home/self/timer_config.json",
            "/home/self/window_state.json"
        ]

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.update_button.pack_forget()
        self.display_current_version()
        self.check_version_file()

    def highlight_step(self, step_index):
        for i, label in enumerate(self.step_labels):
            if i == step_index:
                label.config(bg="yellow")
            else:
                label.config(bg="white")
        self.update_idletasks()

    def display_current_version(self):
        version_file = os.path.join(self.self_path, "versione.csv")
        try:
            with open(version_file, mode='r') as file:
                reader = csv.reader(file)
                current_version_info = "\n".join([" ".join(row) for row in list(reader)[:2]])
                self.current_version_label.config(text=f"Versione Corrente:\n{current_version_info}")
        except Exception as e:
            self.current_version_label.config(text=f"Errore durante la lettura del file versione corrente: {str(e)}")

    def check_updates(self):
        self.status_label.config(text="Controllo aggiornamenti in corso...")
        self.progress.start()
        self.highlight_step(0)
        threading.Thread(target=self.download_from_github).start()

    def download_from_github(self):
        try:
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(self.github_repo, headers=headers)
            response.raise_for_status()
            files = response.json()

            for i, file in enumerate(files):
                download_url = file['download_url']
                file_name = file['name']
                file_response = requests.get(download_url)
                file_response.raise_for_status()
                with open(os.path.join(self.download_path, file_name), 'wb') as f:
                    f.write(file_response.content)
                self.progress.step(100 / len(files))
                self.update_idletasks()

            self.status_label.config(text="Aggiornamenti scaricati da GitHub.")
            self.display_version()
            self.check_version_file()
        except Exception as e:
            self.status_label.config(text=f"Errore durante il download: {str(e)}")
        finally:
            self.progress.stop()

    def display_version(self):
        version_file = os.path.join(self.download_path, "versione.csv")
        try:
            with open(version_file, mode='r') as file:
                reader = csv.reader(file)
                version_info = "\n".join([" ".join(row) for row in list(reader)[:10]])
                self.version_label.config(text=f"Informazioni sulla Versione Scaricata:\n{version_info}")
        except Exception as e:
            self.version_label.config(text=f"Errore durante la lettura del file versione: {str(e)}")

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

    def create_backup(self):
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
        try:
            with zipfile.ZipFile(backup_file, 'w') as backup_zip:
                for file in self.FILES_TO_BACKUP:
                    if os.path.exists(file):
                        backup_zip.write(file, os.path.basename(file))
            return backup_file
        except Exception as e:
            self.status_label.config(text=f"Errore durante la creazione del backup: {str(e)}")
            return None

    def restore_backup(self, backup_file):
        try:
            with zipfile.ZipFile(backup_file, 'r') as backup_zip:
                for file in backup_zip.namelist():
                    source = backup_zip.extract(file, "/tmp")
                    if file in ["clienti.csv", "transactions.csv"]:
                        destination = f"/home/self/Desktop/SELF/{file}"
                    else:
                        destination = f"/home/self/{file}"
                    shutil.move(source, destination)
        except Exception as e:
            self.status_label.config(text=f"Errore durante il ripristino del backup: {str(e)}")

    def check_version_file(self):
        version_file = os.path.join(self.download_path, "versione.csv")
        if os.path.exists(version_file):
            self.update_button.pack(pady=20)
        else:
            self.update_button.pack_forget()

    def show_completion_message(self):
        self.status_label.config(text="Aggiornamento completato con successo! Premi 'Riavvia Ora' per applicare le modifiche.", fg="green")
        self.restart_button.pack(pady=20)  # Mostra il pulsante di riavvio
        for label in self.step_labels:
            label.config(bg="lightgreen")  # Colora tutti i passaggi in verde chiaro

    def restart_application(self):
        self.save_settings()
        self.destroy()
        subprocess.Popen(["bash", os.path.expanduser("~/restart_self.sh")])

    def save_settings(self):
        # Implementa la logica di salvataggio delle impostazioni qui
        pass

    def chiudi_app(self):
        self.destroy()

if __name__ == "__main__":
    app = AggiornaApp()
    app.mainloop()
