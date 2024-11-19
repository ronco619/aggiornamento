import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import csv
import threading
import shutil

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
        
        self.update_button = tk.Button(self, text="Aggiorna", command=self.apply_updates, font=("Arial", 12))
        self.update_button.pack(pady=20)

        self.version_label = tk.Label(self, text="", bg="white", font=("Arial", 12))
        self.version_label.pack(pady=20)

        self.current_version_label = tk.Label(self, text="", bg="white", font=("Arial", 12))
        self.current_version_label.pack(pady=20)

        self.github_repo = "https://api.github.com/repos/ronco619/aggiornamento/contents/"
        self.download_path = "/home/self/Desktop/AGGIORNAMENTI"
        self.self_path = "/home/self/Desktop/SELF"

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        self.update_button.pack_forget()  # Nascondi il pulsante "Aggiorna" inizialmente
        self.display_current_version()
        self.check_version_file()  # Controlla se il file versione.csv è presente

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
            self.check_version_file()  # Ricontrolla il file versione.csv dopo il download
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

    def apply_updates(self):
        self.status_label.config(text="Applicazione degli aggiornamenti in corso...")
        try:
            if os.path.exists(self.self_path):
                shutil.rmtree(self.self_path)
            shutil.move(self.download_path, self.self_path)
            os.makedirs(self.download_path)
            self.status_label.config(text="Aggiornamenti applicati con successo.")
            self.display_current_version()
        except Exception as e:
            self.status_label.config(text=f"Errore durante l'applicazione degli aggiornamenti: {str(e)}")
            os.makedirs(self.download_path)  # Assicurati che la directory di download esista

    def check_version_file(self):
        version_file = os.path.join(self.download_path, "versione.csv")
        if os.path.exists(version_file):
            self.update_button.pack(pady=20)  # Mostra il pulsante "Aggiorna" solo se il file è presente
        else:
            self.update_button.pack_forget()  # Nascondi il pulsante "Aggiorna" se il file non è presente

if __name__ == "__main__":
    app = AggiornaApp()
    app.mainloop()
