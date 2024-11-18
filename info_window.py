import tkinter as tk
from tkinter import ttk
import platform
import psutil
from PIL import Image, ImageTk
import os

class InfoWindow:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Informazioni di Sistema")
        
        # Imposta la finestra a schermo intero
        self.root.attributes('-fullscreen', True)
        
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.root.configure(bg=self.bg_color)

        self.version = "1.0.0"  # Versione del tuo software
        self.image_path = os.path.expanduser("~/Immagini/wb.png")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=("Helvetica", 10), anchor="center")
        style.configure('Title.TLabel', font=("Helvetica", 20, "bold"), anchor="center")
        style.configure('Header.TLabel', font=("Helvetica", 12, "bold"), anchor="center")
        style.configure('TButton', font=("Helvetica", 12), padding=5)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Carica e mostra l'immagine
        if os.path.exists(self.image_path):
            try:
                img = Image.open(self.image_path)
                img = img.resize((400, 250))  # Ridimensionato per adattarsi meglio
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(main_frame, image=photo, background=self.bg_color)
                img_label.image = photo
                img_label.pack(pady=10)
            except Exception as e:
                print(f"Errore nel caricamento dell'immagine: {e}")
        else:
            print(f"Immagine non trovata: {self.image_path}")

        title_label = ttk.Label(main_frame, text="Informazioni di Sistema", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        self.add_info_section(main_frame, "Informazioni Software", [
            f"Versione Software Programma: {self.version}",
            f"Versione Software Sistema: {platform.version()}",
        ])

        self.add_info_section(main_frame, "Informazioni Hardware", [
            f"Versione Python: {platform.python_version()}",
            f"CPU: {platform.processor()}",
            f"Memoria Totale: {psutil.virtual_memory().total / (1024 * 1024 * 1024):.2f} GB",
            f"Memoria Disponibile: {psutil.virtual_memory().available / (1024 * 1024 * 1024):.2f} GB",
            f"Spazio Disco Totale: {psutil.disk_usage('/').total / (1024 * 1024 * 1024):.2f} GB",
            f"Spazio Disco Disponibile: {psutil.disk_usage('/').free / (1024 * 1024 * 1024):.2f} GB"
        ])

        self.add_info_section(main_frame, "Informazioni Aziendali", [
            "Telefono: +39 3314672078",
            "Email: washingbraipr@gmail.com"  
        ])

        close_button = ttk.Button(main_frame, text="CHIUDI", command=self.root.destroy, style='TButton')
        close_button.pack(pady=20)

    def add_info_section(self, parent, title, info_list):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill="x", pady=5)

        header = ttk.Label(section_frame, text=title, style='Header.TLabel')
        header.pack(fill="x")

        for info in info_list:
            info_label = ttk.Label(section_frame, text=info, style='TLabel')
            info_label.pack(fill="x")

    def show(self):
        self.root.grab_set()
        self.root.wait_window()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Nascondi la finestra principale
    info_window = InfoWindow(root)
    info_window.show()