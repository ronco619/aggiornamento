 #https://www.w3schools.com/colors/colors_names.asp tavolozza colori
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk # type: ignore
import os
import threading
import logging
from rfid import RFIDReader
from timer_manager import TimerManager
from database_manager import DatabaseManager
from cliente_nuovo import ClienteNuovo
from datetime import datetime
from banknote_reader import BanknoteReader
from backup_manager import BackupManager
from menu import ConfigMenu
from threading import Timer

import csv
import subprocess
import pygame
from tkinter import messagebox

pygame.mixer.pre_init(frequency=44100, size=-16,channels=2,buffer=4096)
pygame.init()
    #audio
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

subprocess.Popen(["python3", "/home/self/Desktop/SELF/testrfid.py"])
subprocess.Popen(["python3", "/home/self/Desktop/server.py"])


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema di Controllo Accessi")
        self.master.geometry("1024x768")
        logging.info("Chiamata force_fullscreen() in __init__")
        self.master.after(100, self.force_fullscreen)  # Ritardo di 100 ms  
        self.master.bind('<Escape>', self.exit_fullscreen)
        self.master.config(cursor="none")  # Imposta il cursore su "none" all'avvio
        
        # Configurazione del logging
        logging.basicConfig(filename='main_app.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        self.timer_manager = TimerManager(self.master)
        self.rfid_reader = RFIDReader()
        self.db_manager = DatabaseManager()
        self.banknote_reader = BanknoteReader()
        
        # Inizializza e avvia il BackupManager
        self.backup_manager = BackupManager(
            source_file="/home/self/Desktop/SELF/clienti.csv",
            backup_dir="/media/self/BKDB/trabk",
            transactions_file="/home/self/Desktop/SELF/transactions.csv",
            max_backups=30,
            interval_hours=6
        )
        self.start_backup_schedule()
        
        self.recharge_amount = 0
        self.custom_font = font.Font(family="Arial", size=42, weight="bold")

        self.registration_window = None
        self.current_client = None
        
        self.config_card = {"nome": "CONFIGURAZIONE", "cognome": "123456"}
      
        if self.rfid_reader.setup():
            self.setup_main_page()
            #self.print_all_clients()  # Stampa tutti i clienti all'avvio
        else:
            logging.error("Errore nell'inizializzazione del lettore RFID")
            print("Errore nell'inizializzazione del lettore RFID")
        
        self.check_fullscreen()

    def force_fullscreen(self):
        logging.info("Impostazione modalit� fullscreen in force_fullscreen()")
        if not self.master.attributes('-fullscreen'):
            self.master.attributes('-fullscreen', True)

    def exit_fullscreen(self, event=None):
        logging.info("Uscita dalla modalità fullscreen in exit_fullscreen()")
        self.master.attributes('-fullscreen', False)
        self.master.geometry("1024x768")  
        self.master.focus_set() 
    
    def check_fullscreen (self):
        if not self.master.attributes('-fullscreen'):
            self.master.attributes('-fullscreen',True)
            self.master.update()
        self.master.after(100,self.check_fullscreen)
    
    def start_backup_schedule(self):
        try:
            backup_thread = threading.Thread(target=self.backup_manager.start_backup_schedule, daemon=True)
            backup_thread.start()
            logging.info("Thread di backup avviato con successo")
        except Exception as e:
            logging.error(f"Errore nell'avvio del thread di backup: {e}")
            logging.exception("Dettaglio dell'errore:")

    def create_button(self, parent, text, command, bg_color, fg_color="white"):
        button = tk.Button(parent, text=text, font=self.custom_font, fg=fg_color, bg=bg_color, 
                           activebackground=bg_color, activeforeground=fg_color, 
                           command=command, bd=0, relief=tk.FLAT)
        return button

    def setup_main_page(self):
        self.clear_window()
        self.setup_background()
        self.show_main_message()
        self.start_rfid_reading()

    def setup_background(self):
        bg_path = "/home/self/Immagini/sfondo.jpg"
        if os.path.exists(bg_path):
            bg_image = Image.open(bg_path)
            bg_image = bg_image.resize((1024, 800), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(self.master, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            logging.error(f"Errore: L'immagine {bg_path} non esiste.")
            print(f"Errore: L'immagine {bg_path} non esiste.")

    def show_main_message(self):

        custom_font = font.Font(family="Noto Mono", size=80, weight="bold")
        self.main_message = tk.Label(self.master, text="AVVICINARE\nLA TESSERA", 
                                     font=custom_font, fg="gold", bg="#191970")
        self.main_message.place(relx=0.5, rely=0.5, anchor="center")

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_rfid_reading(self):
        self.timer_manager.stop_trpi()  
        self.master.after(100, self.check_rfid)

    def check_rfid(self):
        if self.registration_window:
            self.master.after(100, self.check_rfid)
            return

        uid = self.rfid_reader.read_card()
        if uid:
            self.process_card(uid)
        else:
            self.master.after(100, self.check_rfid)


    def process_card(self, uid):
        logging.info(f"Carta letta: UID = {uid}")
        client = self.db_manager.get_client_by_uid(uid)
        if client:
            logging.info(f"Cliente trovato: Nome = {client['nome']}, Cognome = {client['cognome']}")
            if client['nome'] == self.config_card['nome'] and client['cognome'] == self.config_card['cognome']:
                logging.info("Carta di configurazione riconosciuta, aprendo il menu di configurazione")
                self.show_config_menu()
            else:
                logging.info("Carta cliente normale, mostrando info cliente")
                self.show_client_info(client)
               
                
        else:
            logging.info("Nuovo cliente, avviando procedura di registrazione")
            self.setup_new_client_ui(uid)

    def show_config_menu(self):
        logging.info("Apertura del menu di configurazione")
        config_menu = ConfigMenu(self.master, self.return_to_main_page)
        config_menu.show_config_menu()

    def check_premio(self, nome_cliente):
        premio_file = '/home/self/premi.csv'
        try:
            with open(premio_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cliente'] == nome_cliente and row['approvato'] == 'N':
                        return row['premio']
        except Exception as e:
            logging.error(f"Errore nella lettura del file premi: {e}")
        return None

    def show_premio(self, premio):
        play_audio("/home/self/Desktop/sintesi vocale/premio.mp3")
        self.clear_window()
        self.setup_background()
        
        frame = tk.Frame(self.master, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")


        # Carica e mostra l'immagine
        img_path = "/home/self/Immagini/coppa oro.jpg"
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=photo, bg="black")
        img_label.image = photo
        img_label.pack(pady=20)

        congrats_label = tk.Label(frame, text="CONGRATULAZIONI", font=self.custom_font, fg="yellow", bg="black")
        congrats_label.pack(pady=20)

        congrats_label = tk.Label(frame, text="PREMIO FEDELTA", font=self.custom_font, fg="yellow", bg="black")
        congrats_label.pack(pady=20)

        premio_label = tk.Label(frame, text=f"Premio: \u20ac {premio}", font=self.custom_font, fg="white", bg="black")
        premio_label.pack(pady=20)

        def blink():
            if congrats_label.winfo_exists():
                current_color = congrats_label.cget("fg")
                next_color = "yellow" if current_color == "black" else "black"
                congrats_label.config(fg=next_color)
            self.master.after(500, blink)

        blink()

       # Chiudi dopo 5 secondi
        self.master.after(5000, self.close_premio_screen)

    def close_premio_screen(self):
        self.clear_window()
        self.return_to_main_page()

    def update_premio_status(self, nome_cliente):
        premio_file = '/home/self/premi.csv'
        temp_file = '/home/self/premi_temp.csv'
        try:
            with open(premio_file, 'r') as file, open(temp_file, 'w', newline='') as temp:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(temp, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['cliente'] == nome_cliente and row['approvato'] == 'N':
                        row['approvato'] = 'S'
                    writer.writerow(row)
            os.replace(temp_file, premio_file)
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento del file premi: {e}")

    def show_client_info(self, client):
        logging.info(f"Mostrando info per il cliente: {client['nome']} {client['cognome']}")
        play_audio("/home/self/Desktop/sintesi vocale/per_ricaricare.mp3")
        # Verifica se il cliente ha un premio
        nome_completo = f"{client['nome']} {client['cognome']}"
        premio = self.check_premio(nome_completo)
        if premio:
            self.show_premio(premio)
            self.update_premio_status(nome_completo)
            return

        self.clear_window()
        self.setup_background()

        self.info_frame = tk.Frame(self.master, bg="black")
        self.info_frame.place(relx=0.5, rely=0.5, anchor="center")

        greeting = self.get_greeting()

        self.greeting_label = tk.Label(self.info_frame, text=f"{greeting}", font=self.custom_font, fg="yellow", bg="black")
        self.greeting_label.pack(pady=10)

        self.name_label = tk.Label(self.info_frame, text=f"{client['nome']}", font=self.custom_font, fg="white", bg="black")
        self.name_label.pack(pady=10)

        balance = float(client['euro'])
        self.balance_label = tk.Label(self.info_frame, text=f" \u20ac  {balance:.2f}", font=self.custom_font, fg="green", bg="black")
        self.balance_label.pack(pady=10)

        self.recharge_button = self.create_button(self.info_frame, "RICARICA", self.start_recharge, "green")
        self.recharge_button.pack(pady=20)

        self.trpi_label = tk.Label(self.master, text="", font=font.Font(family="Arial", size=24), fg="yellow", bg="black")
        self.trpi_label.pack(side="bottom", pady=20)

        self.timer_manager.start_trpi(self.trpi_label, self.return_to_main_page)

        self.current_client = client
   
    def start_recharge(self):
        logging.info("Avvio procedura di ricarica")
        play_audio("/home/self/Desktop/sintesi vocale/ricarica.mp3")

        self.timer_manager.stop_trpi()
        self.banknote_reader.set_callback(self.on_banknote_inserted)
        self.banknote_reader.activate()

        self.greeting_label.pack_forget()
        self.name_label.pack_forget()
        self.recharge_button.pack_forget()

        tk.Label(self.info_frame, text="Inserisci le banconote ", font=self.custom_font, fg="white", bg="black").pack(pady=10)

        self.amount_label = tk.Label(self.info_frame, text="Importo inserito:  \u20ac 0,00", font=self.custom_font, fg="green", bg="black")
        self.amount_label.pack(pady=10)

        self.stop_button = self.create_button(self.info_frame, "TERMINA RICARICA", self.stop_recharge, "red")
        self.stop_button.pack(pady=20)

        self.recharge_amount = 0

        # Avvia il timeout di ricarica
        self.start_recharge_timeout()

    def on_banknote_inserted(self, amount):
        if self.recharge_amount + amount > 50.00:
            self.amount_label.config(text=f"Importo massimo raggiunto:  \u20ac 50,00")
            self.banknote_reader.deactivate()

        else:
            self.recharge_amount += amount
            self.amount_label.config(text=f"Importo inserito:  \u20ac {self.recharge_amount:.2f}")

    def start_recharge_timeout(self):
        self.timer_manager.start_recharge_timeout(self.stop_recharge)

    def check_promo(self, amount):
        promo_file = '/home/self/promo_attivo.csv'
        try:
            with open(promo_file, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:
                    promo_row = rows[1]
                    if len(promo_row) >= 5 and promo_row[0] == 'si' and promo_row[1] == 'si' and promo_row[4] == 'si':
                        amount_column = min(int(amount / 5) + 4, len(promo_row) - 1)
                        return float(promo_row[amount_column])
        except Exception as e:
            logging.error(f"Errore nella lettura del file promozioni: {e}")
        return 0.0

    def show_promo_message(self, promo_amount):
        # Salva lo stato attuale dell'interfaccia
        self.clear_window()
        self.setup_background()
        promo_frame = tk.Frame(self.master, bg="black")
        promo_frame.place(relx=0.5, rely=0.5, anchor="center")
        promo_font = font.Font(family="Arial", size=60, weight="bold")

        message = f"HAI RICEVUTO\nUNA PROMOZIONE DI \n\u20ac{promo_amount:.2f}!"
        
        label = tk.Label(promo_frame, text=message, font=promo_font, fg="yellow", bg="black")
        label.pack(expand=True)
        self.master.update()
        self.master.after(2000, self.continue_after_promo)

    def continue_after_promo(self):
        # Continua con il flusso normale dopo aver mostrato il messaggio della promozione
        stampa_ricevute = self.check_receipt_printing_option()
        if stampa_ricevute:
            play_audio("/home/self/Desktop/sintesi vocale/ricevuta.mp3")
            self.show_print_receipt_button()
        else:
            self.return_to_main_page()



    def stop_recharge(self):
        logging.info("Terminazione procedura di ricarica")
        play_audio("/home/self/Desktop/sintesi vocale/arr&gra.mp3")

        self.timer_manager.reset_trto()

        self.banknote_reader.deactivate()
        if self.current_client and self.recharge_amount > 0:
            promo_amount = self.check_promo(self.recharge_amount)
            total_recharge = self.recharge_amount + promo_amount

            new_balance = float(self.current_client['euro']) + total_recharge
            self.current_client['euro'] = f"{new_balance:.2f}"
            self.db_manager.update_client_balance(self.current_client['uid'], new_balance)
            self.backup_manager.log_transaction(total_recharge, f"{self.current_client['nome']} {self.current_client['cognome']}")
            
            logging.info(f"Ricarica completata. Importo: �{self.recharge_amount:.2f}, Promozione: �{promo_amount:.2f}, Totale: �{total_recharge:.2f}, Nuovo saldo: �{new_balance:.2f}")

            # Mostra un messaggio all'utente sulla promozione
            if promo_amount > 0:
                self.show_promo_message(promo_amount)
            else:
                self.continue_after_promo()
        else:
            self.return_to_main_page()    

    def check_receipt_printing_option(self):
        try:
            with open('/home/self/config_scontrino.csv', 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['stampa_ricevute'].lower() == 'true':
                        return True
        except Exception as e:
            logging.error(f"Errore nella lettura del file di configurazione: {e}")
        return False

    def show_print_receipt_button(self):
        logging.debug("Mostrando il pulsante per la stampa della ricevuta")
        self.clear_window()

        frame = tk.Frame(self.master, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        image_path = "/home/self/Immagini/scontrino.png"
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(frame, image=photo, bg="black")
        img_label.image = photo
        img_label.pack(side=tk.LEFT, padx=(0, 20))

        self.print_button = self.create_button(frame, "STAMPA RICEVUTA", self.print_receipt, "blue")
        self.print_button.pack(side=tk.LEFT)

        self.close_timer = Timer(5.0, self.auto_close_receipt_screen)
        self.close_timer.start()

    def show_print_receipt_button(self):
        self.clear_window()

        # Crea un frame per contenere il pulsante e l'immagine
        frame = tk.Frame(self.master, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Carica e ridimensiona l'immagine
        image_path = "/home/self/Immagini/scontrino.png"
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.LANCZOS)  # Ridimensiona a 200x200
        photo = ImageTk.PhotoImage(img)

        # Crea un label per l'immagine
        img_label = tk.Label(frame, image=photo, bg="black")
        img_label.image = photo  # Mantieni un riferimento!
        img_label.pack(side=tk.LEFT, padx=(0, 20))  # Aggiungi un po' di spazio tra l'immagine e il pulsante

        # Crea il pulsante "STAMPA RICEVUTA"
        self.print_button = self.create_button(frame, "STAMPA RICEVUTA", self.print_receipt, "blue")
        self.print_button.pack(side=tk.LEFT)
    
        self.close_timer = Timer(5.0, self.auto_close_receipt_screen)
        self.close_timer.start()

    def auto_close_receipt_screen(self):
        logging.info("Chiusura automatica della schermata di stampa ricevuta")
        self.return_to_main_page()

    def print_receipt(self):
        # Annulla il timer di chiusura
        if hasattr(self, 'close_timer'):
            self.close_timer.cancel()

        try:
            env_path = "/home/self/pi-rfid/env/bin/activate"
            script_path = "/home/self/Desktop/SELF/stampa_ricevuta.py"
            command = f"source {env_path} && python {script_path}"

            subprocess.run(command, shell=True, executable='/bin/bash', check=True)
            logging.info("Ricevuta stampata con successo")
        except Exception as e:
            logging.error(f"Errore durante la stampa della ricevuta: {e}")
        finally:
            self.return_to_main_page()

    def return_to_main_page(self):
        # Annulla il timer di chiusura se esiste
        if hasattr(self, 'close_timer'):
            self.close_timer.cancel()

        # Rimuovi il pulsante di stampa se esiste
        if hasattr(self, 'print_button'):
            self.print_button.destroy()

        # Resetta le variabili di ricarica
        self.recharge_amount = 0

        # Riavvia il timer TRPI
        self.timer_manager.start_trpi(self.trpi_label, self.return_to_main_page)

        logging.info("Ritorno alla pagina principale")
        self.show_client_info(self.current_client)

        self.master.after(100,self.force_fullscreen)

    def get_greeting(self):
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "BUON GIORNO"
        elif 12 <= current_hour < 18:
            return "BUON POMERIGGIO"
        else:
            return "BUONA SERA"

    def setup_new_client_ui(self, uid):
        logging.info(f"Avvio procedura di registrazione per nuovo cliente. UID: {uid}")
        play_audio("/home/self/Desktop/sintesi vocale/nome.mp3")
        self.timer_manager.stop_trpi()
        self.registration_window = ClienteNuovo(self.master, uid, self.db_manager, self.on_registration_complete, self.timer_manager)

    def on_registration_complete(self):
        logging.info("Registrazione nuovo cliente completata")
        play_audio("/home/self/Desktop/sintesi vocale/registrato.mp3")

        self.registration_window = None
        self.return_to_main_page()

    def return_to_main_page(self):
        logging.info("Ritorno alla pagina principale")
        self.setup_main_page()

    def cleanup(self):
        logging.info("Pulizia e chiusura dell'applicazione")
        self.rfid_reader.cleanup()
        if self.registration_window:
            self.registration_window.destroy()

    def print_all_clients(self):
        clients = self.db_manager.get_all_clients()
        logging.info("Lista di tutti i clienti:")
        for client in clients:
            logging.info(f"UID: {client['uid']}, Nome: {client['nome']}, Cognome: {client['cognome']}")

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()

if __name__ == "__main__":
    main()
