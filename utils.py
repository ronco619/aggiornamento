import tkinter as tk
from tkinter import ttk
import logging

def show_loading(parent, message="Caricamento in corso..."):
    loading_window = tk.Toplevel(parent)
    loading_window.title("Caricamento")
    loading_window.geometry("300x100")
    loading_window.resizable(False, False)
    loading_window.transient(parent)

    ttk.Label(loading_window, text=message).pack(pady=10)
    progress_bar = ttk.Progressbar(loading_window, mode="indeterminate")
    progress_bar.pack(pady=10, padx=20, fill=tk.X)
    progress_bar.start()

    loading_window.update()
    
    try:
        loading_window.grab_set()
    except tk.TclError:
        logging.warning("Impossibile impostare il grab sulla finestra di caricamento")

    return loading_window

def close_loading(loading_window):
    if loading_window and loading_window.winfo_exists():
        loading_window.destroy()