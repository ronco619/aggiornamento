import tkinter as tk
import json
import os

class TimerManager:
    def __init__(self, master):
        self.master = master
        self.config_file = os.path.expanduser("~/timer_settings.json")
        
        # Carica le impostazioni salvate o usa i valori di default
        settings = self.load_settings()
        
        # Timer TRPI (Timer Ritorno Pagina Iniziale)
        self.trpi_active = False
        self.trpi_remaining = settings.get("trpi", 7)
        self.trpi_default = settings.get("trpi", 7)
        self.trpi_label = None
        self.trpi_callback = None
        self.trpi_after_id = None

        # Timer TASP (Timer Annullamento Senza Pressione)
        self.tasp_active = False
        self.tasp_remaining = settings.get("tasp", 15)
        self.tasp_default = settings.get("tasp", 15)
        self.tasp_label = None
        self.tasp_callback = None
        self.tasp_after_id = None

        # Timer TRTO (Timer Ricarica Timeout)
        self.trto_active = False
        self.trto_remaining = settings.get("trto", 120)  # Imposta il timeout a 120 secondi di default
        self.trto_default = settings.get("trto", 120)
        self.trto_label = None
        self.trto_callback = None
        self.trto_after_id = None

    def load_settings(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Ritorna un dizionario vuoto se il file non esiste o è invalido

    def save_settings(self):
        settings = {
            "trpi": self.trpi_default,
            "tasp": self.tasp_default,
            "trto": self.trto_default
        }
        with open(self.config_file, 'w') as f:
            json.dump(settings, f)

    # Metodi per TRPI
    def start_trpi(self, label, callback):
        self.stop_trpi()  # Ferma il timer esistente, se presente
        self.trpi_active = True
        self.trpi_remaining = self.trpi_default
        self.trpi_label = label
        self.trpi_callback = callback
        self.update_trpi()

    def stop_trpi(self):
        self.trpi_active = False
        if self.trpi_label and self.trpi_label.winfo_exists():
            self.trpi_label.config(text="")
        if self.trpi_after_id:
            self.master.after_cancel(self.trpi_after_id)
            self.trpi_after_id = None
        self.trpi_label = None
        self.trpi_callback = None


    def update_trpi(self):
        if not self.trpi_active or not self.trpi_label or not self.trpi_label.winfo_exists():
            return

        if self.trpi_remaining <= 0:
            self.trpi_label.config(text="Ritorno alla pagina principale...")
            if self.trpi_callback:
                self.master.after(1000, self.trpi_callback)
            self.stop_trpi()
            return

        self.trpi_label.config(text=f"Ritorno alla pagina principale in: {self.trpi_remaining}s")
        self.trpi_remaining -= 1
        self.trpi_after_id = self.master.after(1000, self.update_trpi)

    def reset_trpi(self):
        if self.trpi_active and self.trpi_label and self.trpi_label.winfo_exists():
            self.trpi_remaining = self.trpi_default
            if self.trpi_after_id:
                self.master.after_cancel(self.trpi_after_id)
            self.update_trpi()

    # Metodi per TASP
    def start_tasp(self, label, callback):
        self.stop_tasp()  # Ferma il timer esistente, se presente
        self.tasp_active = True
        self.tasp_remaining = self.tasp_default
        self.tasp_label = label
        self.tasp_callback = callback
        self.update_tasp()

    def stop_tasp(self):
        self.tasp_active = False
        if self.tasp_label and self.tasp_label.winfo_exists():
            self.tasp_label.config(text="")
        if self.tasp_after_id:
            self.master.after_cancel(self.tasp_after_id)
            self.tasp_after_id = None
        self.tasp_label = None
        self.tasp_callback = None

    def update_tasp(self):
        if not self.tasp_active or not self.tasp_label or not self.tasp_label.winfo_exists():
            return

        if self.tasp_remaining <= 0:
            self.tasp_label.config(text="Operazione annullata")
            if self.tasp_callback:
                self.master.after(1000, self.tasp_callback)  # Chiamiamo il callback dopo 1 secondo
            self.stop_tasp()
            return

        self.tasp_label.config(text=f"Tempo rimanente: {self.tasp_remaining}s")
        self.tasp_remaining -= 1
        self.tasp_after_id = self.master.after(1000, self.update_tasp)

    def reset_tasp(self):
        if self.tasp_active and self.tasp_label and self.tasp_label.winfo_exists():
            self.tasp_remaining = self.tasp_default
            if self.tasp_after_id:
                self.master.after_cancel(self.tasp_after_id)
            self.update_tasp()

    def get_trto_value(self):
        return self.trto_default

    def set_trto_value(self, value):
        self.trto_default = value
        self.trto_remaining = value
        self.save_settings()
        
    def start_recharge_timeout(self, callback):
        self.stop_trto()  # Ferma il timer esistente, se presente
        self.trto_active = True
        self.trto_remaining = self.trto_default
        self.trto_callback = callback
        self.update_trto()

    def stop_trto(self):
        self.trto_active = False
        if self.trto_label and self.trto_label.winfo_exists():
            self.trto_label.config(text="")
        if self.trto_after_id:
            self.master.after_cancel(self.trto_after_id)
            self.trto_after_id = None
        self.trto_label = None
        self.trto_callback = None

    def reset_trto(self):
        self.stop_trto()
        self.trto_remaining = self.trto_default

    def update_trto(self):
        if not self.trto_active:
            return
        if self.trto_remaining <= 0:
            if self.trto_callback:
                self.master.after(1000, self.trto_callback)
            self.stop_trto()
            return

        self.trto_remaining -= 1
        self.trto_after_id = self.master.after(1000, self.update_trto)   

       # Metodi per ottenere e impostare i valori dei timer
    def get_trpi_value(self):
        return self.trpi_default

    def set_trpi_value(self, value):
        self.trpi_default = value
        self.trpi_remaining = value
        self.save_settings()  # Salva le impostazioni dopo la modifica

    def get_tasp_value(self):
        return self.tasp_default

    def set_tasp_value(self, value):
        self.tasp_default = value
        self.tasp_remaining = value
        self.save_settings()  # Salva le impostazioni dopo la modifica

    def get_trto_value(self):
        return self.trto_default

    def set_trto_value(self, value):
        self.trto_default = value
        self.trto_remaining = value
        self.save_settings()  # Salva le impostazioni dopo la modifica

    def reset_to_defaults(self):
        self.trpi_remaining = self.trpi_default
        self.tasp_remaining = self.tasp_defaul

