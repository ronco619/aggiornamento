
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import pygame


class VoiceManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Management")
        self.master.geometry("600x400")
        self.voice_enabled = tk.BooleanVar()
        self.voice_entries = []

        self.setup_ui()

    def setup_ui(self):
        tk.Checkbutton(self.master, text="Enable Voice Function", variable=self.voice_enabled).pack(pady=10)
        
        self.voice_frame = tk.Frame(self.master)
        self.voice_frame.pack(pady=10)

        self.add_voice_entry()

        tk.Button(self.master, text="Add Voice", command=self.add_voice_entry).pack(pady=5)
        tk.Button(self.master, text="Save and Exit", command=self.save_and_exit).pack(pady=10)

    def add_voice_entry(self):
        entry_frame = tk.Frame(self.voice_frame)
        entry_frame.pack(pady=5)

        tk.Label(entry_frame, text="Voice Name:").pack(side=tk.LEFT)
        voice_name = tk.Entry(entry_frame)
        voice_name.pack(side=tk.LEFT, padx=5)

        tk.Label(entry_frame, text="File Path:").pack(side=tk.LEFT)
        voice_path = tk.Entry(entry_frame)
        voice_path.pack(side=tk.LEFT, padx=5)

        tk.Button(entry_frame, text="Browse", command=lambda: self.browse_file(voice_path)).pack(side=tk.LEFT, padx=5)
        tk.Button(entry_frame, text="Play", command=lambda: self.play_voice(voice_path.get())).pack(side=tk.LEFT, padx=5)
        
        self.voice_entries.append((voice_name, voice_path))

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def play_voice(self, file_path):
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def save_and_exit(self):
        config_dir = "/home/self/Desktop/sintesi vocale"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        config_file = os.path.join(config_dir, "voice_config.csv")

        with open(config_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Voice Name", "File Path"])

            for voice_name, voice_path in self.voice_entries:
                writer.writerow([voice_name.get(), voice_path.get()])

        messagebox.showinfo("Saved", "Configuration saved successfully!")
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceManager(root)
    root.mainloop()
