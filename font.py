import tkinter as tk
from tkinter import font, ttk

class FontSelector:
    def __init__(self, master):
        self.master = master
        master.title("Selettore di Font")
        master.geometry("1024x600")  # Adattato al tuo schermo

        self.sample_text = "ABCDEFGHIJKLMNOPQRST"  # 20 lettere
        self.fonts = list(font.families())
        self.fonts.sort()

        # Frame principale
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas e Scrollbar
        self.canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack elementi
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_font_labels()

    def create_font_labels(self):
        for font_name in self.fonts:
            try:
                label_font = font.Font(family=font_name, size=14)
                label = ttk.Label(self.scrollable_frame, text=f"{font_name}: {self.sample_text}", font=label_font)
                label.pack(pady=5)
            except:
                print(f"Impossibile caricare il font: {font_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FontSelector(root)
    root.mainloop()