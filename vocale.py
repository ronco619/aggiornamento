import tkinter as tk
from tkinter import messagebox
import os
import subprocess

class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Volume Control")
        self.root.geometry("1024x800")
        self.root.attributes('-fullscreen', True)
        
        self.create_widgets()
        self.set_initial_volume()
        
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Volume Control", font=("Arial", 24))
        self.label.pack(pady=20)
        
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", length=600, width=30)
        self.volume_scale.pack(pady=20)
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_volume, font=("Arial", 18))
        self.save_button.pack(pady=10)
        
        self.close_button = tk.Button(self.root, text="Close", command=self.close_app, font=("Arial", 18))
        self.close_button.pack(pady=10)
        
    def set_initial_volume(self):
        result = subprocess.run(['amixer', 'get', 'Master'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        volume = int(output.split('[')[1].split('%')[0])
        self.volume_scale.set(volume)
        
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
