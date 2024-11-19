import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import pygame

class GestioneVoci:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestione Voci")
        self.master.geometry("1024x800")
        self.master.attributes('-fullscreen', True)
        self.voce_abilitata = tk.BooleanVar()
        self.voci_entries = []
        self.voce_config = {}

        self.setup_ui()
        self.carica_config()

    def setup_ui(self):
        tk.Checkbutton(self.master, text="Abilita Funzione Voce", variable=self.voce_abilitata).pack(pady=10)

        self.voci_frame = tk.Frame(self.master)
        self.voci_frame.pack(pady=10)

        tk.Button(self.master, text="Aggiungi Voce", command=self.aggiungi_voce_entry).pack(pady=5)
        tk.Button(self.master, text="Salva ed Esci", command=self.salva_ed_esci).pack(pady=10)
        tk.Button(self.master, text="Chiudi", command=self.chiudi_app).pack(pady=10)

    def aggiungi_voce_entry(self, nome_voce="", percorso_voce=""):
        entry_frame = tk.Frame(self.voci_frame)
        entry_frame.pack(pady=5)

        tk.Label(entry_frame, text="Nome Voce:").pack(side=tk.LEFT)
        nome_voce_entry = tk.Entry(entry_frame)
        nome_voce_entry.pack(side=tk.LEFT, padx=5)
        nome_voce_entry.insert(0, nome_voce)

        tk.Label(entry_frame, text="Percorso File:").pack(side=tk.LEFT)
        percorso_voce_entry = tk.Entry(entry_frame)
        percorso_voce_entry.pack(side=tk.LEFT, padx=5)
        percorso_voce_entry.insert(0, percorso_voce)

        tk.Button(entry_frame, text="Sfoglia", command=lambda: self.sfoglia_file(percorso_voce_entry)).pack(side=tk.LEFT, padx=5)
        tk.Button(entry_frame, text="Riproduci", command=lambda: self.riproduci_voce(nome_voce_entry.get())).pack(side=tk.LEFT, padx=5)

        self.voci_entries.append((nome_voce_entry, percorso_voce_entry))

    def sfoglia_file(self, entry):
        file_path = filedialog.askopenfilename(filetypes=[("File Audio", "*.mp3 *.wav")])
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def riproduci_voce(self, nome_voce):
        if nome_voce not in self.voce_config or not self.voce_abilitata.get():
            messagebox.showerror("Errore", "Voce non abilitata o non trovata!")
            return

        file_path = self.voce_config[nome_voce]["File Path"]
        if not os.path.exists(file_path):
            messagebox.showerror("Errore", "File non trovato!")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def salva_ed_esci(self):
        self.salva_config()
        self.master.quit()

    def salva_config(self):
        config_dir = "/home/self/Desktop/sintesi vocale"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        config_file = os.path.join(config_dir, "config_voci.csv")

        with open(config_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nome Voce", "Percorso File", "Voce Abilitata"])
            writer.writerow([self.voce_abilitata.get()])

            for nome_voce, percorso_voce in self.voci_entries:
                writer.writerow([nome_voce.get(), percorso_voce.get()])

    def carica_config(self):
        try:
            with open('voice_config.csv', mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if len(row) < 3:
                        continue  # Skip rows that do not have at least 3 columns
                    self.voce_config[row[0]] = {"File Path": row[1], "Voice Enabled": row[2] == "True"}
        except FileNotFoundError:
            messagebox.showerror("Errore", "File voice_config.csv non trovato!")

    def chiudi_app(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestioneVoci(root)
    root.mainloop()
