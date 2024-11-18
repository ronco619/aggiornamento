# censimento.py

import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os

class CensimentoPage:
    def __init__(self, master, uid):
        self.master = master
        self.master.title("Censimento")
        self.master.geometry("1024x900")

        self.uid = uid
        self.bg_photo = None  # Inizializza bg_photo come attributo della classe
        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        bg_path = "/home/self/Immagini/sfondo.jpg"
        if not os.path.exists(bg_path):
            print(f"Errore: L'immagine {bg_path} non esiste.")
            return

        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((1024, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)  # Assegna a self.bg_photo

        self.canvas = tk.Canvas(self.master, width=1024, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def setup_ui(self):
        custom_font = font.Font(family="Arial", size=40, weight="bold")

        # Testo per il titolo
        self.canvas.create_text(824, 280, text="UID Tessera", font=custom_font, fill="white")

        # Testo per visualizzare l'UID
        self.canvas.create_text(824, 420, text=self.uid, font=custom_font, fill="yellow")

    def show(self):
        self.master.mainloop()