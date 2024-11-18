import tkinter as tk
from tkinter import ttk
from timer_manager import TimerManager
from virtual_number import VirtualNumberKeyboard
import subprocess
import os

class TimerSettingsPage(tk.Frame):
    def __init__(self, master, timer_manager):
        super().__init__(master)
        self.timer_manager = timer_manager
        self.master = master
        self.configure(bg='#f0f0f0')
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.active_entry = None

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 14), background='#f0f0f0')
        style.configure('TEntry', font=('Arial', 14))
        style.configure('TButton', font=('Arial', 18))
        style.configure('Active.TEntry', fieldbackground='light yellow')
        style.configure('Red.TButton', background='red', foreground='white', font=('Arial', 18))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Impostazioni Timer", font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        ttk.Label(main_frame, text="Timer Ritorno Pagina Iniziale (TRPI):").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.trpi_entry = ttk.Entry(main_frame, width=15)
        self.trpi_entry.grid(row=1, column=1, padx=10, pady=10)
        self.trpi_entry.insert(0, str(self.timer_manager.get_trpi_value()))
        self.trpi_entry.bind("<Button-1>", lambda event: self.show_keyboard(self.trpi_entry))

        ttk.Label(main_frame, text="Timer Annullamento Senza Pressione (TASP):").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.tasp_entry = ttk.Entry(main_frame, width=15)
        self.tasp_entry.grid(row=2, column=1, padx=10, pady=10)
        self.tasp_entry.insert(0, str(self.timer_manager.get_tasp_value()))
        self.tasp_entry.bind("<Button-1>", lambda event: self.show_keyboard(self.tasp_entry))
#
        ttk.Label(main_frame, text="Timer Ricarica Timeout (TRTO):").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.trto_entry = ttk.Entry(main_frame, width=15)
        self.trto_entry.grid(row=3, column=1, padx=10, pady=10)
        self.trto_entry.insert(0, str(self.timer_manager.get_trto_value()))
        self.trto_entry.bind("<Button-1>", lambda event: self.show_keyboard(self.trto_entry))

#
        self.keyboard_frame = ttk.Frame(main_frame)
        self.keyboard_frame.grid(row=3, column=0, columnspan=2, pady=20)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Aggiungi i pulsanti "ESCI" e "SALVA E RIAVVIA"
        exit_button = ttk.Button(self.master, text="ESCI", command=self.master.destroy, width=20)
        exit_button.place(x=100, rely=0.85, anchor='w')

        save_restart_button = ttk.Button(self.master, text="SALVA E RIAVVIA", command=self.save_and_restart, width=20, style='Red.TButton')
        save_restart_button.place(x=100, rely=0.92, anchor='w')

    def show_keyboard(self, entry):
        if self.active_entry:
            self.active_entry.configure(style='TEntry')
        self.active_entry = entry
        entry.configure(style='Active.TEntry')

        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        
        keyboard = VirtualNumberKeyboard(self.keyboard_frame, entry, on_enter=self.hide_keyboard, on_key_press=self.update_entry)
        keyboard.pack(pady=20)

    def hide_keyboard(self):
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        if self.active_entry:
            self.active_entry.configure(style='TEntry')
        self.active_entry = None

    def update_entry(self):
        pass

    def save_and_restart(self):
        self.save_settings()
        self.master.destroy()  # Chiude tutte le finestre
        subprocess.Popen(["bash", os.path.expanduser("~/restart_self.sh")])  # Esegue lo script di riavvio

    def save_settings(self):
        try:
            trpi_value = int(self.trpi_entry.get())
            tasp_value = int(self.tasp_entry.get())
            trto_value = int(self.trto_entry.get() )
            
            self.timer_manager.set_trpi_value(trpi_value)
            self.timer_manager.set_tasp_value(tasp_value)
            self.timer_manager.set_trto_value(trto_value)
        except ValueError:
            pass  # Ignora gli errori di conversione

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Impostazioni Timer")
    
    root.overrideredirect(True)
    root.geometry("1024x800+0+0")
    
    timer_manager = TimerManager(root)
    settings_page = TimerSettingsPage(root, timer_manager)
    
    root.mainloop()