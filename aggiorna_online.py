import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import csv
import threading
import shutil

class UpdateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Update System")
        self.geometry("800x600")
        self.configure(bg="white")
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self, text="Press 'Check for Updates' to start.", bg="white", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.check_button = tk.Button(self, text="Check for Updates", command=self.check_updates, font=("Arial", 12))
        self.check_button.pack(pady=20)
        
        self.update_button = tk.Button(self, text="Update", command=self.apply_updates, font=("Arial", 12))
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

        self.display_current_version()

    def display_current_version(self):
        version_file = os.path.join(self.self_path, "versione.csv")
        try:
            with open(version_file, mode='r') as file:
                reader = csv.reader(file)
                current_version_info = "\n".join([" ".join(row) for row in reader])
                self.current_version_label.config(text=f"Current Version Info:\n{current_version_info}")
        except Exception as e:
            self.current_version_label.config(text=f"Error reading current version file: {str(e)}")

    def check_updates(self):
        self.status_label.config(text="Checking for updates...")
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

            self.status_label.config(text="Updates downloaded from GitHub.")
            self.display_version()
        except Exception as e:
            self.status_label.config(text=f"Error during download: {str(e)}")
        finally:
            self.progress.stop()

    def display_version(self):
        version_file = os.path.join(self.download_path, "versione.csv")
        try:
            with open(version_file, mode='r') as file:
                reader = csv.reader(file)
                version_info = "\n".join([" ".join(row) for row in reader])
                self.version_label.config(text=f"Downloaded Version Info:\n{version_info}")
        except Exception as e:
            self.version_label.config(text=f"Error reading version file: {str(e)}")

    def apply_updates(self):
        self.status_label.config(text="Applying updates...")
        try:
            if os.path.exists(self.self_path):
                shutil.rmtree(self.self_path)
            shutil.move(self.download_path, self.self_path)
            os.makedirs(self.download_path)
            self.status_label.config(text="Updates applied successfully.")
            self.display_current_version()
        except Exception as e:
            self.status_label.config(text=f"Error applying updates: {str(e)}")
            os.makedirs(self.download_path)  # Ensure the download directory exists

if __name__ == "__main__":
    app = UpdateApp()
    app.mainloop()
