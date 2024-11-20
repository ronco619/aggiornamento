import tkinter as tk
from tkinter import messagebox
import os

class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Volume Control")
        self.root.geometry("1024x800")
        self.root.attributes('-fullscreen', True)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Volume Control", font=("Arial", 24))
        self.label.pack(pady=20)
        
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", length=400)
        self.volume_scale.pack(pady=20)
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_volume, font=("Arial", 18))
        self.save_button.pack(pady=10)
        
        self.close_button = tk.Button(self.root, text="Close", command=self.close_app, font=("Arial", 18))
        self.close_button.pack(pady=10)
        
    def save_volume(self):
        volume = self.volume_scale.get()
        os.system(f"amixer set Master {volume}%")
        messagebox.showinfo("Volume Control", f"Volume set to {volume}%")
        
    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeApp(root)
    root.mainloop()
