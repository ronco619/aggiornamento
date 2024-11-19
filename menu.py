#menu.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from PIL import Image, ImageTk
import os
from database_manager import DatabaseManager
from datetime import datetime, timedelta
import csv
import calendar
import locale
from calendar import day_name, month_name
from dateutil.relativedelta import relativedelta
from tkinter import messagebox
import subprocess  #lanciare finestra esterna
from tkinter import ttk, messagebox
from virtual_number import VirtualNumberKeyboard
from timer_manager import TimerManager
from info_window import InfoWindow

from dialogs import TouchFriendlyDialog, TouchFriendlyConfirmDialog
from utils import show_loading, close_loading
import logging
import subprocess
import os
# Imposta la localizzazione italiana
locale.setlocale(locale.LC_TIME, 'it_IT.utf8')

class ConfigMenu:
    def __init__(self, master, return_callback):
        self.master = master
        self.return_callback = return_callback
        self.db_manager = DatabaseManager()
      
        self.timer_manager = TimerManager(self.master)
        class ConfigMenu:
            self.clicked_buttons = set()
        
        # Definizione di stili e colori
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.button_color = "#3498DB"
        self.button_active_color = "#2980B9"
        self.font_large = ("Helvetica", 24, "bold")
        self.font_medium = ("Helvetica", 20)
        self.font_small = ("Helvetica", 16)
        #
        self.highlight_color = "#FFFF00"  # Giallo


        # Ottieni le dimensioni dello schermo
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

    def show_config_menu(self):
        if hasattr(self, 'config_window') and self.config_window.winfo_exists():
            self.config_window.lift()
            self.config_window.focus_force()
            return

        self.config_window = tk.Toplevel(self.master)
        self.config_window.title("Menu Configurazione")
        #self.config_window.overrideredirect(True)
    
        self.set_fullscreen(self.config_window)
        self.config_window.configure(bg=self.bg_color)
        
        self.setup_styles()

        main_frame = ttk.Frame(self.config_window, style='Main.TFrame')
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(main_frame, text="Menu Configurazione", style='Title.TLabel')
        title_label.pack(pady=(0, 40))

        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(expand=True, fill="both")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        buttons = [
            ("MENU TOTALI", self.show_totals_menu),
            ("MENU CLIENTI", self.open_clienti_menu), 
            ("CONFIGURAZIONI", self.show_configurations),
            ("TIMER", self.open_timer_menu),
            ("ESCI", self.close_config_menu),  
            ("INFO", self.show_info_window)
            
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(button_frame, text=text, command=command, style='LargeMenu.TButton')
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=20)

        for i in range(3):  # Assumendo 3 righe di pulsanti
            button_frame.rowconfigure(i, weight=1)

        self.config_window.protocol("WM_DELETE_WINDOW", self.close_config_menu)
        self.config_window.transient(self.master)
        self.config_window.grab_set()

    def handle_button_click(self, button_text, command):
        if button_text not in self.clicked_buttons:
            self.clicked_buttons.add(button_text)
            command()
            # Disabilita il pulsante dopo il clic
            for child in self.config_window.winfo_children():
                if isinstance(child, ttk.Frame):
                    for btn in child.winfo_children():
                        if isinstance(btn, ttk.Button) and btn['text'] == button_text:
                            btn.state(['disabled'])

    def setup_styles(self):
        style = ttk.Style(self.master)
        style.theme_use('clam')

        style.configure('Main.TFrame', background=self.bg_color)

        style.configure('Title.TLabel', 
                        font=("Helvetica", 30, "bold"), 
                        background=self.bg_color, 
                        foreground=self.fg_color)

        style.configure('LargeMenu.TButton', 
                        font=("Helvetica", 24), 
                        background=self.button_color, 
                        foreground=self.fg_color,
                        padding=(24, 24))

        style.map('LargeMenu.TButton', 
                  background=[('active', self.button_active_color)])


        style.configure('CurrentDay.TLabel', 
                        font=("Helvetica", 20, "bold"),
                        background=self.bg_color, 
                        foreground=self.fg_color)

        style.configure('Grid.TFrame', 
                        background="white")

        style.configure('GridContent.TLabel', 
                        font=("Helvetica", 14),
                        background="white", 
                        foreground="#2C3E50")
        #colore totali giorno,oggi                     
        style.configure('CurrentDay.TLabel', 
                        font=("Helvetica", 20, "bold"),
                        background=self.bg_color, 
                        foreground=self.highlight_color)    
        #menu timers 
        style.configure('Grid.TFrame', background="white")
        style.configure('Grid.TLabel', background="white", font=("Helvetica", 14))
        style.configure('Grid.TEntry', font=("Helvetica", 14))

        #menu clienti
        style.configure('GridHeader.TLabel', 
                        font=("Helvetica", 14, "bold"),
                        background="lightgray", 
                        padding=5)
        style.configure('GridContent.TLabel', 
                        font=("Helvetica", 12),
                        background="white", 
                        padding=5)
        style.configure('Grid.TEntry', 
                        font=("Helvetica", 12))

    def close_config_menu(self):
        if hasattr(self, 'config_window') and self.config_window.winfo_exists():
            self.clicked_buttons.clear()  # Resetta lo stato dei pulsanti
            self.config_window.grab_release()
            self.config_window.destroy()
        self.return_callback()

    def set_fullscreen(self, window):
        window.attributes('-fullscreen', True)
        window.geometry(f"{self.screen_width}x{self.screen_height}+10+10")

    def show_totals_menu(self):
        if hasattr(self, 'totals_window') and self.totals_window.winfo_exists():
            self.totals_window.lift()
            self.totals_window.focus_force()
            return

        self.totals_window = tk.Toplevel(self.master)
        self.totals_window.title("Menu Totali")
        self.set_fullscreen(self.totals_window)
        self.totals_window.configure(bg=self.bg_color)
    
        main_frame = ttk.Frame(self.totals_window, style='Main.TFrame')
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(main_frame, text="Menu Totali", style='Title.TLabel')
        title_label.pack(pady=(0, 40))

        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(expand=True, fill="both")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        buttons = [
            ("TOTALI ASSOLUTI", self.show_absolute_totals),
            ("TOTALI MENSILI", self.show_monthly_totals),
            ("TOTALI GIORNALIERI", self.show_daily_totals),
            ("TOTALI PERSONALIZZATI", self.show_custom_period_totals),
            ("INDIETRO", self.close_totals_menu)
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(button_frame, text=text, command=command, style='LargeMenu.TButton')
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=20)

        for i in range(3):  # Assumendo 3 righe di pulsanti
            button_frame.rowconfigure(i, weight=1)

        self.totals_window.protocol("WM_DELETE_WINDOW", self.close_totals_menu)
        self.totals_window.transient(self.master)
        self.totals_window.grab_set()

    def close_totals_menu(self):
        if hasattr(self, 'totals_window') and self.totals_window.winfo_exists():
            self.totals_window.grab_release()
            self.totals_window.destroy()

    def set_fullscreen(self, window):
        window.attributes('-fullscreen', True)
        window.geometry(f"{self.screen_width}x{self.screen_height}+10+10")

    def create_sub_window(self, title, content_function=None):
        sub_window = tk.Toplevel(self.config_window)
        sub_window.title(title)
        self.set_fullscreen(sub_window)
        sub_window.configure(bg=self.bg_color)
        if content_function:
            content_function(sub_window)
        return sub_window
    
    def open_clienti_menu(self):
        subprocess.Popen(["python3", "/home/self/Desktop/SELF/rep_clienti_menu.py"])


    def show_configurations(self):
        config_window = self.create_sub_window("Configurazioni")
        self.resize_and_center_window(config_window, 1024, 800)


        # Rimuovi la chiamata a overrideredirect(True)
        # config_window.overrideredirect(True)

        # Imposta la finestra a schermo intero
        self.set_fullscreen(config_window)

        # Ridimensionare e posizionare correttamente la finestra
        self.resize_and_center_window(config_window)

        main_frame = ttk.Frame(config_window, style='Main.TFrame')
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(main_frame, text="Configurazioni", style='Title.TLabel')
        title_label.pack(pady=(0, 40))

        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(expand=True, fill="both")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        config_buttons = [
            ("RIAVVIO", self.reboot_system),
            ("GESTIONE BCK", self.manage_backups),
            ("PAGAMENTI", self.manage_payments),
            ("PROMOZIONI", self.manage_promotions),
            ("GESTIONE CREDITO", self.manage_credit),
            ("AGGIORNAMENTI", self.check_updates),
            ("STAMPANTE",self.config_stampante),
            ("INDIETRO", config_window.destroy)
        ]

        for i, (text, command) in enumerate(config_buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(button_frame, text=text, command=command, style='LargeMenu.TButton')
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=20)

        for i in range(4):  # 4 righe per i pulsanti
            button_frame.rowconfigure(i, weight=1)

    def resize_and_center_window(self, window, offset_x=0, offset_y=-100):
        window.update_idletasks()  # Assicurati che le dimensioni siano aggiornate
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2) + offset_x
        y = (screen_height // 2) - (height // 2) + offset_y
        window.geometry(f"{width}x{height}+{x}+{y}")
    

    def reboot_system(self):
        try:
            
            self.master.destroy()  # Chiude tutte le finestre
            subprocess.Popen(["bash", os.path.expanduser("~/restart_self.sh")])
        except Exception as e:
            print(f"Errore durante l'esecuzione dello script: {str(e)}")

    def config_stampante(self):
        subprocess.Popen(["python3","/home/self/Desktop/SELF/conf_stampante.py"])

    def manage_backups(self):
        subprocess.Popen(["python3","/home/self/Desktop/SELF/bck_manual.py"])

    def manage_payments(self):
        # Implementa la gestione dei pagamenti
        pass

    def manage_credit(self):
        subprocess.Popen(["python3", "/home/self/Desktop/SELF/credito.py"])


    def manage_promotions(self):
        promo_window = tk.Toplevel(self.master)
        promo_window.title("Gestione Promozioni")
        #promo_window.overrideredirect(True)
        
        self.set_fullscreen(promo_window)
        promo_window.configure(bg=self.bg_color)

        main_frame = ttk.Frame(promo_window, style='Main.TFrame')
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(main_frame, text="Gestione Promozioni", style='Title.TLabel')
        title_label.pack(pady=(0, 40))

        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(expand=True, fill="both")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Bottoni per 'premio', 'ricarica' e 'esci'
        buttons = [
            ("PREMIO", lambda: subprocess.Popen(["python3", "/home/self/Desktop/SELF/classifica.py", "-topmost", "1"])),
            ("RICARICA", lambda: subprocess.Popen(["python3", "/home/self/Desktop/SELF/promo_ricarica.py", "-topmost", "1"])),  # Sostituisci "ricarica.py" con il nome corretto del file
            ("ESCI", promo_window.destroy)
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(button_frame, text=text, command=command, style='LargeMenu.TButton')
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=20)

        for i in range(2):  # Assumendo 2 righe di pulsanti
            button_frame.rowconfigure(i, weight=1)

        promo_window.protocol("WM_DELETE_WINDOW", promo_window.destroy)
        promo_window.transient(self.master)
        promo_window.grab_set()
    
    

    def check_updates(self):
        subprocess.Popen(["python3", "/home/self/Desktop/SELF/aggiorna_online.py"])


    def open_timer_menu(self):
        subprocess.Popen(["python3", "/home/self/Desktop/SELF/timer_menu.py"])

        #TIMER MENU FINE
    def show_info_window(self):
        print("Inizio della funzione show_info_window")
        try:
            info_window = InfoWindow(self.master)
            info_window.show()
            print("Finestra delle informazioni creata con successo")
        except Exception as e:
            print(f"Errore in show_info_window: {str(e)}")
            import traceback
            traceback.print_exc()
        print("Fine della funzione show_info_window")

    def create_sub_window(self, title):
        sub_window = tk.Toplevel(self.config_window)
        sub_window.title(title)
        self.set_fullscreen(sub_window)
        sub_window.config(bg=self.bg_color)
        return sub_window

    def show_absolute_totals(self):
        try:
            total = self.calculate_total_from_csv()
            self.show_total_window("Totali Assoluti", f"Totale Assoluto: €{total:.2f}")
        except Exception as e:
            self.show_error_window(str(e))

    def show_monthly_totals(self):
        try:
            today = datetime.now()
            monthly_totals = []

            for i in range(7):
                date = today - relativedelta(months=i)
                total = self.calculate_monthly_total(date.year, date.month)
                monthly_totals.append((date, total))

            self.show_monthly_totals_window(monthly_totals)
        except Exception as e:
            self.show_error_window(str(e))

    def show_monthly_totals_window(self, monthly_totals):
        total_window = tk.Toplevel(self.master)
        total_window.title("Totali Mensili")
        total_window.geometry("800x600")
        total_window.configure(bg=self.bg_color)

        content_frame = ttk.Frame(total_window, style='Main.TFrame')
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(content_frame, text="Totali degli Ultimi 7 Mesi", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # Mese corrente
        current_month, current_total = monthly_totals[0]
        current_month_label = ttk.Label(content_frame, 
                                        text=f"{current_month.strftime('%B')}: €{current_total:.2f}", 
                                        style='CurrentDay.TLabel')
        current_month_label.pack(pady=(0, 20))

        # Griglia per gli altri mesi
        grid_frame = ttk.Frame(content_frame, style='Grid.TFrame')
        grid_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, (date, total) in enumerate(monthly_totals[1:], start=1):
            month_label = ttk.Label(grid_frame, 
                                    text=f"{date.strftime('%B %Y')}", 
                                    style='GridContent.TLabel')
            month_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            total_label = ttk.Label(grid_frame, 
                                    text=f"€{total:.2f}", 
                                    style='GridContent.TLabel')
            total_label.grid(row=i, column=1, padx=10, pady=5, sticky="e")

        close_button = ttk.Button(content_frame, 
                                  text="CHIUDI", 
                                  command=total_window.destroy, 
                                  style='LargeMenu.TButton')
        close_button.pack(pady=20)

        total_window.transient(self.master)
        total_window.grab_set()
        self.master.wait_window(total_window)

    def calculate_monthly_total(self, year, month):
        total = 0
        try:
            with open('/home/self/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trans_date = datetime.strptime(row['Data'], '%d/%m/%y')
                    if trans_date.year == year and trans_date.month == month:
                        total += float(row['Valore'])
        except Exception as e:
            raise Exception(f"Errore nel calcolo del totale mensile: {str(e)}")
        return total

    def show_daily_totals(self):
        try:
            today = datetime.now().date()
            daily_totals = []

            for i in range(7):
                date = today - timedelta(days=i)
                total = self.calculate_daily_total(date)
                daily_totals.append((date, total))

            self.show_daily_totals_window(daily_totals)
        except Exception as e:
            self.show_error_window(str(e))

    def show_daily_totals_window(self, daily_totals):
        total_window = tk.Toplevel(self.master)
        total_window.title("Totali Giornalieri")
        total_window.geometry("800x600")
        total_window.configure(bg=self.bg_color)
    
        content_frame = ttk.Frame(total_window, style='Main.TFrame')
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(content_frame, text="Totali degli Ultimi 7 Giorni", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # Giorno corrente
        
        current_day, current_total = daily_totals[0]
        current_day_label = ttk.Label(content_frame, 
                                      text=f"Oggi, {current_day.strftime('%d %B')} - {current_day.strftime('%A')}: €{current_total:.2f}", 
                                      style='CurrentDay.TLabel')
        current_day_label.pack(pady=(0, 20))

        # Griglia per gli altri giorni
        grid_frame = ttk.Frame(content_frame, style='Grid.TFrame')
        grid_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, (date, total) in enumerate(daily_totals[1:], start=1):
            day_label = ttk.Label(grid_frame, 
                                  text=f"{date.strftime('%A')}, {date.strftime('%d %B')}", 
                                  style='GridContent.TLabel')
            day_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            total_label = ttk.Label(grid_frame, 
                                    text=f"€{total:.2f}", 
                                    style='GridContent.TLabel')
            total_label.grid(row=i, column=1, padx=10, pady=5, sticky="e")

        close_button = ttk.Button(content_frame, 
                                  text="CHIUDI", 
                                  command=total_window.destroy, 
                                  style='LargeMenu.TButton')
        close_button.pack(pady=20)

        total_window.transient(self.master)
        total_window.grab_set()
        self.master.wait_window(total_window)

    def show_total_window(self, title, message):
        total_window = tk.Toplevel(self.master)
        total_window.title(title)
        total_window.geometry("800x600")
        total_window.configure(bg=self.bg_color)
        
        content_frame = ttk.Frame(total_window, style='Main.TFrame')
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        total_label = ttk.Label(content_frame, text=message, style='Title.TLabel')
        total_label.pack(pady=50)
        
        close_button = ttk.Button(content_frame, 
                                  text="CHIUDI", 
                                  command=total_window.destroy, 
                                  style='LargeMenu.TButton')
        close_button.pack(pady=20)
        
        total_window.transient(self.master)
        total_window.grab_set()
        self.master.wait_window(total_window)

    def calculate_total_from_csv(self):
        total = 0
        try:
            with open('/home/self/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    total += float(row['Valore'])
        except FileNotFoundError:
            raise Exception("File transactions.csv non trovato in /home/self/")
        except KeyError:
            raise Exception("Il campo 'Valore' non è presente nel file CSV")
        except ValueError:
            raise Exception("Errore nella conversione del valore a numero")
        except Exception as e:
            raise Exception(f"Si è verificato un errore durante la lettura del file: {str(e)}")
        return total

    def calculate_monthly_total(self, year, month):
        total = 0
        try:
            with open('/home/self/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = datetime.strptime(row['Data'], '%d/%m/%y')
                    if date.year == year and date.month == month:
                        total += float(row['Valore'])
        except Exception as e:
            raise Exception(f"Errore nel calcolo del totale mensile: {str(e)}")
        return total

    def calculate_daily_total(self, date):
        total = 0
        try:
            with open('/home/self/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trans_date = datetime.strptime(row['Data'], '%d/%m/%y').date()
                    if trans_date == date:
                        total += float(row['Valore'])
        except Exception as e:
            raise Exception(f"Errore nel calcolo del totale giornaliero: {str(e)}")
        return total

    def show_error_window(self, error_message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Errore")
        error_window.geometry("400x200")
        error_window.configure(bg=self.bg_color)
        
        error_label = ttk.Label(error_window, 
                                text=f"Si è verificato un errore:\n{error_message}", 
                                style='Title.TLabel',
                                wraplength=380)
        error_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        close_button = ttk.Button(error_window, 
                                  text="CHIUDI", 
                                  command=error_window.destroy, 
                                  style='LargeMenu.TButton')
        close_button.pack(pady=20)
        
        error_window.transient(self.master)
        error_window.grab_set()
        self.master.wait_window(error_window)

    def show_custom_period_totals(self):
        custom_window = tk.Toplevel(self.master)
        custom_window.title("Totali Personalizzati")
        self.set_fullscreen(custom_window)
        custom_window.configure(bg=self.bg_color)

        content_frame = ttk.Frame(custom_window, style='Main.TFrame')
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = ttk.Label(content_frame, text="Seleziona Periodo", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        calendars_frame = ttk.Frame(content_frame, style='Main.TFrame')
        calendars_frame.pack(pady=20)

        # Calendario "Da"
        from_label = ttk.Label(calendars_frame, text="Da:", style='GridContent.TLabel')
        from_label.grid(row=0, column=0, padx=(0, 20))
        from_cal = Calendar(calendars_frame, selectmode='day', date_pattern='dd/mm/yyyy', 
                            font=("Helvetica", 16), 
                            selectbackground='orange',
                            background=self.button_color,
                            foreground=self.fg_color,
                            bordercolor=self.button_color,
                            headersbackground=self.button_color,
                            headersforeground=self.fg_color,
                            weekendbackground=self.button_active_color,
                            weekendforeground=self.fg_color,
                            othermonthwebackground=self.bg_color,
                            othermonthweforeground='gray')
        from_cal.grid(row=1, column=0, padx=(0, 20), pady=10)

        # Calendario "A"
        to_label = ttk.Label(calendars_frame, text="A:", style='GridContent.TLabel')
        to_label.grid(row=0, column=1, padx=(20, 0))
        to_cal = Calendar(calendars_frame, selectmode='day', date_pattern='dd/mm/yyyy',
                          font=("Helvetica", 16),
                          selectbackground='orange',
                          background=self.button_color,
                          foreground=self.fg_color,
                          bordercolor=self.button_color,
                          headersbackground=self.button_color,
                          headersforeground=self.fg_color,
                          weekendbackground=self.button_active_color,
                          weekendforeground=self.fg_color,
                          othermonthwebackground=self.bg_color,
                          othermonthweforeground='gray')
        to_cal.grid(row=1, column=1, padx=(20, 0), pady=10)

        def highlight_days(*args):
            from_date = datetime.strptime(from_cal.get_date(), '%d/%m/%Y').date()
            to_date = datetime.strptime(to_cal.get_date(), '%d/%m/%Y').date()

            if from_date > to_date:
                messagebox.showerror("Errore", "La data 'Da' non può essere successiva alla data 'A'")
                return

            for cal in [from_cal, to_cal]:
                cal.calevent_remove('all')
                cal.tag_config('selected', background='orange')

            current_date = from_date
            while current_date <= to_date:
                from_cal.calevent_create(current_date, 'selected', 'selected')
                to_cal.calevent_create(current_date, 'selected', 'selected')
                current_date += timedelta(days=1)

        from_cal.bind("<<CalendarSelected>>", highlight_days)
        to_cal.bind("<<CalendarSelected>>", highlight_days)

        style = ttk.Style()
        style.configure("LargeResult.TLabel", 
                        font=("Helvetica", 24, "bold"),
                        background=self.bg_color,
                        foreground=self.highlight_color)

        result_label = ttk.Label(content_frame, text="", style='LargeResult.TLabel')
        result_label.pack(pady=30)

        def calculate_totals():
            from_date = datetime.strptime(from_cal.get_date(), '%d/%m/%Y').date()
            to_date = datetime.strptime(to_cal.get_date(), '%d/%m/%Y').date()

            if from_date > to_date:
                messagebox.showerror("Errore", "La data 'Da' non può essere successiva alla data 'A'")
                return

            try:
                total = self.calculate_custom_period_total(from_date, to_date)
                result_label.config(text=f"Totale per il periodo selezionato:\n                         €{total:.2f}")
            except Exception as e:
                messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

        button_frame = ttk.Frame(content_frame, style='Main.TFrame')
        button_frame.pack(pady=30)

        calculate_button = ttk.Button(button_frame, text="Calcola Totali", command=calculate_totals, style='LargeMenu.TButton')
        calculate_button.pack(side=tk.LEFT, padx=10)

        close_button = ttk.Button(button_frame, text="CHIUDI", command=custom_window.destroy, style='LargeMenu.TButton')
        close_button.pack(side=tk.LEFT, padx=10)

        custom_window.protocol("WM_DELETE_WINDOW", custom_window.destroy)
        custom_window.transient(self.master)
        custom_window.grab_set()
        self.master.wait_window(custom_window)

    def calculate_custom_period_total(self, from_date, to_date):
        total = 0
        try:
            with open('/home/self/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trans_date = datetime.strptime(row['Data'], '%d/%m/%y').date()
                    if from_date <= trans_date <= to_date:
                        total += float(row['Valore'])
        except Exception as e:
            raise Exception(f"Errore nel calcolo del totale personalizzato: {str(e)}")
        return total

    def calculate_totals():
        from_date = datetime.strptime(from_cal.get_date(), '%d/%m/%Y').date()
        to_date = datetime.strptime(to_cal.get_date(), '%d/%m/%Y').date()

        if from_date > to_date:
            messagebox.showerror("Errore", "La data 'Da' non può essere successiva alla data 'A'")
        return

        total = self.calculate_custom_period_total(from_date, to_date)
        result_label.config(text=f"Totale per il periodo selezionato: €{total:.2f}")

        calculate_button = ttk.Button(content_frame, text="Calcola Totali", command=calculate_totals, style='LargeMenu.TButton')
        calculate_button.pack(pady=20)

        close_button = ttk.Button(content_frame, text="CHIUDI", command=custom_window.destroy, style='LargeMenu.TButton')
        close_button.pack(pady=20)

        custom_window.transient(self.master)
        custom_window.grab_set()
        self.master.wait_window(custom_window)


        return datetime.now()  # Placeholder
