import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import os
import time
import csv
import requests
import zipfile
from datetime import datetime

class AggiornaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaccia di Aggiornamento")
        self.geometry("1024x800")
        self.configure(bg="white")
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self, text="Premi 'Aggiorna' per iniziare.", bg="white", font=("Arial", 14))
        self.status_label.pack(pady=20)
        
        self.update_button = tk.Button(self, text="Aggiorna", command=self.applica_aggiornamenti, font=("Arial", 12))
        self.update_button.pack(pady=20)
        
        self.usb_button = tk.Button(self, text="Aggiorna da USB", command=self.aggiorna_da_usb, font=("Arial", 12))
        self.usb_button.pack(pady=20)
        
        self.github_button = tk.Button(self, text="Aggiorna da GitHub", command=self.aggiorna_da_github, font=("Arial", 12))
        self.github_button.pack(pady=20)

        self.exit_button = tk.Button(self, text="Chiudi", command=self.quit, font=("Arial", 12))
        self.exit_button.pack(pady=20)
        
        self.version_file = "/home/self/Desktop/AGGIORNAMENTI/versione.csv"
        self.current_version = self.leggi_versione()

    def applica_aggiornamenti(self):
        self.status_label.config(text="Applicando aggiornamenti...")
        try:
            # Rimuovi la vecchia cartella e sostituisci con la nuova
            if os.path.exists("/home/self/Desktop/SELF"):
                subprocess.run(["rm", "-rf", "/home/self/Desktop/SELF"])
            subprocess.run(["mv", "/home/self/Desktop/AGGIORNAMENTI", "/home/self/Desktop/SELF"])
            
            # Aggiorna il file della versione
            new_version = "1.0.1"  # Questo dovrebbe essere dinamico
            self.scrivi_versione(new_version)
            
            self.status_label.config(text="Aggiornamenti applicati con successo.")
        except Exception as e:
            self.status_label.config(text=f"Errore durante l'aggiornamento: {str(e)}")
    
    def aggiorna_da_usb(self):
        self.status_label.config(text="Aggiornamento da USB in corso...")
        usb_path = "/media/usb/self.zip"
        try:
            if os.path.exists(usb_path):
                if os.path.exists("/home/self/Desktop/SELF"):
                    subprocess.run(["rm", "-rf", "/home/self/Desktop/SELF"])
                
                # Estrai il contenuto di self.zip
                with zipfile.ZipFile(usb_path, 'r') as zip_ref:
                    zip_ref.extractall("/home/self/Desktop/SELF")
                
                # Leggi la versione dalla chiavetta USB
                version_file = "/home/self/Desktop/SELF/versione.csv"
                new_version = self.leggi_versione(version_file)

                # Aggiorna il file della versione locale
                self.scrivi_versione(new_version[1])
                
                self.status_label.config(text="Aggiornamento da USB completato con successo.")
            else:
                self.status_label.config(text="File self.zip non trovato sulla chiavetta USB.")
        except Exception as e:
            self.status_label.config(text=f"Errore durante l'aggiornamento da USB: {str(e)}")

    def aggiorna_da_github(self):
        self.status_label.config(text="Scaricando aggiornamenti da GitHub...")
        self.progress.start()
        threading.Thread(target=self.scarica_da_github).start()
        
    def scarica_da_github(self):
        try:
            repo_url = "https://github.com/ronco619/aggiornamenti"
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(repo_url, headers=headers)
            response.raise_for_status()
            files = response.json()

            for file in files:
                download_url = file['download_url']
                file_name = file['name']
                response = requests.get(download_url)
                with open(f"/home/self/Desktop/AGGIORNAMENTI/{file_name}", 'wb') as f:
                    f.write(response.content)
                self.progress.step(100 / len(files))
                self.update_idletasks()

            self.status_label.config(text="Aggiornamenti scaricati da GitHub.")
        except Exception as e:
            self.status_label.config(text=f"Errore durante il download da GitHub: {str(e)}")
        finally:
            self.progress.stop()

    def leggi_versione(self, version_file=None):
        if version_file is None:
            version_file = self.version_file
        try:
            with open(version_file, mode='r') as file:
                reader = csv.reader(file)
                return next(reader)
        except Exception as e:
            self.status_label.config(text=f"Errore durante la lettura della versione: {str(e)}")
            return None
    
    def scrivi_versione(self, version):
        try:
            with open("/home/self/Desktop/SELF/versione.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d"), version])
        except Exception as e:
            self.status_label.config(text=f"Errore durante la scrittura della versione: {str(e)}")

if __name__ == "__main__":
    app = AggiornaApp()
    app.mainloop()
