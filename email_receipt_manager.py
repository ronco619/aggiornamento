import csv
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import font

class EmailReceiptManager:
    def __init__(self, master, client_data, recharge_amount):
        self.master = master
        self.client_data = client_data
        self.recharge_amount = recharge_amount
        self.custom_font = font.Font(family="Arial", size=24, weight="bold")

    def check_email_receipt_enabled(self):
        try:
            with open('/home/self/ricev_mail.csv', 'r') as file:
                reader = csv.reader(file)
                first_row = next(reader)
                return first_row[0].lower() == 'si'
        except Exception as e:
            logging.error(f"Errore nella lettura del file ricev_mail.csv: {e}")
            return False

    def show_email_receipt_button(self):
        self.clear_window()
        frame = tk.Frame(self.master, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.email_button = tk.Button(frame, text="INVIO RICEVUTA", font=self.custom_font, 
                                      fg="white", bg="blue", command=self.send_email_receipt)
        self.email_button.pack(pady=20)

    def send_email_receipt(self):
        try:
            email = self.get_email_from_csv(self.client_data['uid'])
            if not email:
                logging.error("Indirizzo email non trovato per questo cliente")
                return

            config = self.load_email_config()

            msg = MIMEMultipart()
            msg['From'] = config['sender_email']
            msg['To'] = email
            msg['Subject'] = config.get('subject', "Ricevuta di ricarica")

            body = self.create_receipt_body(config)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(config['smtp_server'], int(config['smtp_port'])) as server:
                server.starttls()
                server.login(config['sender_email'], config['sender_password'])
                server.send_message(msg)

            logging.info(f"Ricevuta inviata via email a {email}")
        except Exception as e:
            logging.error(f"Errore nell'invio della ricevuta via email: {e}")

    def get_email_from_csv(self, uid):
        try:
            with open('/home/self/ricev_mail.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['uid'] == uid:
                        return row['mail']
        except Exception as e:
            logging.error(f"Errore nella lettura dell'email dal file CSV: {e}")
        return None

    def load_email_config(self):
        config = {}
        try:
            with open('/home/self/config_mail', 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    config[key.strip()] = value.strip()
        except Exception as e:
            logging.error(f"Errore nel caricamento della configurazione email: {e}")
        return config

    def create_receipt_body(self, config):
        body = config.get('body_template', "Ricevuta di ricarica\n\n")
        body += f"Cliente: {self.client_data['nome']} {self.client_data['cognome']}\n"
        body += f"Importo ricaricato: €{self.recharge_amount:.2f}\n"
        body += f"Nuovo saldo: €{self.client_data['euro']}\n"
        return body

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    @staticmethod
    def show_email_config_ui(master):
        config_window = tk.Toplevel(master)
        config_window.geometry("1024x600")
        config_window.attributes('-fullscreen', True)

        frame = tk.Frame(config_window, bg="black")
        frame.pack(expand=True, fill="both")

        entries = {}
        fields = ['sender_email', 'sender_password', 'smtp_server', 'smtp_port', 'subject', 'body_template']

        for field in fields:
            label = tk.Label(frame, text=field.replace('_', ' ').title(), bg="black", fg="white")
            label.pack()
            entry = tk.Entry(frame, width=50)
            entry.pack()
            entries[field] = entry

        save_button = tk.Button(frame, text="Salva", command=lambda: EmailReceiptManager.save_email_config(entries, config_window))
        save_button.pack(pady=20)

        exit_button = tk.Button(frame, text="Esci", command=config_window.destroy)
        exit_button.pack()

    @staticmethod
    def save_email_config(entries, window):
        config = {field: entry.get() for field, entry in entries.items()}
        try:
            with open('/home/self/config_mail', 'w') as file:
                for key, value in config.items():
                    file.write(f"{key}={value}\n")
            logging.info("Configurazione email salvata con successo")
        except Exception as e:
            logging.error(f"Errore nel salvataggio della configurazione email: {e}")
        window.destroy()
