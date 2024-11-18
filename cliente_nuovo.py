# cliente_nuovo.py

import tkinter as tk
from tkinter import font as tkfont
from virtual_keyboard import SimpleVirtualKeyboard

class ClienteNuovo(tk.Toplevel):
    def __init__(self, parent, uid, db_manager, on_complete, timer_manager):
        super().__init__(parent)
        self.uid = uid
        self.db_manager = db_manager
        self.on_complete = on_complete
        self.timer_manager = timer_manager
        
        self.title("Registrazione Nuovo Cliente")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.setup_ui()
        
    def setup_ui(self):
        main_font = tkfont.Font(family="Arial", size=18)
        
        tk.Label(self, text="Registrazione Nuovo Cliente", font=("Arial", 24, "bold")).pack(pady=20)
        
        # Frame per i campi di input
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        
        # Nome
        tk.Label(input_frame, text="Nome*:", font=main_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nome_entry = tk.Entry(input_frame, font=main_font)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Cognome
        tk.Label(input_frame, text="Cognome*:", font=main_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cognome_entry = tk.Entry(input_frame, font=main_font)
        self.cognome_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Messaggio di stato
        self.status_label = tk.Label(self, text="", font=main_font)
        self.status_label.pack(pady=10)
        
        # Timer TASP
        self.tasp_label = tk.Label(self, text="", font=main_font, fg="red")
        self.tasp_label.pack(pady=5)
        
        # Tastiera virtuale
        self.keyboard_frame = tk.Frame(self)
        self.keyboard_frame.pack(pady=10)
        self.current_entry = self.nome_entry
        self.show_virtual_keyboard()
        
        self.nome_entry.focus_set()
        
        # Avvia il timer TASP
        self.timer_manager.start_tasp(self.tasp_label, self.on_tasp_timeout)

    def show_virtual_keyboard(self):
        if hasattr(self, 'keyboard'):
            self.keyboard.destroy()
        self.keyboard = SimpleVirtualKeyboard(self.keyboard_frame, self.current_entry, on_enter=self.on_keyboard_enter, on_key_press=self.timer_manager.reset_tasp)
        self.keyboard.pack()
        
    def on_keyboard_enter(self):
        self.timer_manager.reset_tasp()
        if self.current_entry == self.nome_entry:
            if not self.nome_entry.get().strip():
                self.status_label.config(text="Nome obbligatorio per procedere", fg="red")
                return
            self.current_entry = self.cognome_entry
            self.status_label.config(text="")
        elif self.current_entry == self.cognome_entry:
            self.register_client()
        self.current_entry.focus_set()
        self.show_virtual_keyboard()
        
    def register_client(self):
        nome = self.nome_entry.get().strip()
        cognome = self.cognome_entry.get().strip()
        
        if not nome or not cognome:
            self.status_label.config(text="Errore: Nome e Cognome sono obbligatori", fg="red")
            return
        
        try:
            self.db_manager.add_client(nome, cognome, self.uid, "0", "0")
            self.status_label.config(text="Cliente registrato con successo!", fg="green")
            self.timer_manager.stop_tasp()
            self.after(2000, self.close_window)
        except Exception as e:
            self.status_label.config(text=f"Errore durante la registrazione: {str(e)}", fg="red")

    def on_tasp_timeout(self):
        self.close_window()

    def close_window(self):
        self.timer_manager.stop_tasp()
        self.destroy()
        self.on_complete()