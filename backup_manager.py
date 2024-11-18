# backup_manager.py
import os
import shutil
import time
import csv
import logging
from datetime import datetime, timedelta

class BackupManager:
    def __init__(self, source_file, backup_dir, transactions_file, max_backups=30, interval_hours=6):
        self.source_file = source_file
        self.backup_dir = backup_dir
        self.transactions_file = transactions_file
        self.max_backups = max_backups
        self.interval_hours = interval_hours

        logging.basicConfig(filename='backup_manager.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self.clients_backup_dir = os.path.join(self.backup_dir, "CLIENTI")
        self.transactions_backup_dir = os.path.join(self.backup_dir, "TRANS")

        self.ensure_directories()
        self.ensure_transactions_file()

    def ensure_directories(self):
        try:
            os.makedirs(self.clients_backup_dir, exist_ok=True)
            os.makedirs(self.transactions_backup_dir, exist_ok=True)
            logging.info(f"Directory di backup assicurate: {self.clients_backup_dir}, {self.transactions_backup_dir}")
        except Exception as e:
            logging.error(f"Errore nella creazione delle directory di backup: {e}")

    def ensure_transactions_file(self):
        if not os.path.exists(self.transactions_file):
            try:
                with open(self.transactions_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Data", "Ora", "Valore", "Cliente", "Tipo"])
                logging.info(f"File delle transazioni creato: {self.transactions_file}")
            except Exception as e:
                logging.error(f"Errore nella creazione del file delle transazioni: {e}")

    def start_backup_schedule(self):
        while True:
            try:
                self.create_backup()
                self.cleanup_old_backups()
            except Exception as e:
                logging.error(f"Errore durante il backup: {e}")
            time.sleep(self.interval_hours * 3600)  # Sleep for interval_hours

    def create_backup(self):
        try:
            timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
            
            # Backup del file clienti
            clients_backup_filename = f"bck-{timestamp}.csv"
            clients_backup_path = os.path.join(self.clients_backup_dir, clients_backup_filename)
            shutil.copy2(self.source_file, clients_backup_path)
            logging.info(f"Backup clienti creato: {clients_backup_path}")

            # Backup delle transazioni
            transactions_backup_filename = f"transactions-{timestamp}.csv"
            transactions_backup_path = os.path.join(self.transactions_backup_dir, transactions_backup_filename)
            shutil.copy2(self.transactions_file, transactions_backup_path)
            logging.info(f"Backup delle transazioni creato: {transactions_backup_path}")
        except Exception as e:
            logging.error(f"Errore durante la creazione del backup: {e}")

    def cleanup_old_backups(self):
        try:
            self._cleanup_directory(self.clients_backup_dir, "bck-")
            self._cleanup_directory(self.transactions_backup_dir, "transactions-")
        except Exception as e:
            logging.error(f"Errore durante la pulizia dei vecchi backup: {e}")

    def _cleanup_directory(self, directory, prefix):
        backups = [f for f in os.listdir(directory) if f.startswith(prefix)]
        backups.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        while len(backups) > self.max_backups:
            oldest_backup = backups.pop()
            os.remove(os.path.join(directory, oldest_backup))
            logging.info(f"Rimosso vecchio backup: {os.path.join(directory, oldest_backup)}")

    def log_transaction(self, amount, client_name):
        try:
            timestamp = datetime.now()
            date = timestamp.strftime("%d/%m/%y")
            time = timestamp.strftime("%H:%M:%S")

            with open(self.transactions_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, time, amount, client_name, "Banconote inserite per ricarica"])

            logging.info(f"Transazione registrata: {amount} € per {client_name}")
        except Exception as e:
            logging.error(f"Errore durante la registrazione della transazione: {e}")

    def get_transactions(self, start_date=None, end_date=None):
        transactions = []
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    date = datetime.strptime(row[0], "%d/%m/%y")
                    if (start_date is None or date >= start_date) and (end_date is None or date <= end_date):
                        transactions.append({
                            "data": row[0],
                            "ora": row[1],
                            "valore": float(row[2]),
                            "cliente": row[3],
                            "tipo": row[4]
                        })
        except Exception as e:
            logging.error(f"Errore durante il recupero delle transazioni: {e}")
        return transactions

    def get_total_transactions(self, start_date=None, end_date=None):
        total = 0
        transactions = self.get_transactions(start_date, end_date)
        for transaction in transactions:
            total += transaction["valore"]
        return total

    def get_transactions_by_client(self, client_name, start_date=None, end_date=None):
        return [t for t in self.get_transactions(start_date, end_date) if t["cliente"] == client_name]

    def get_total_by_client(self, client_name, start_date=None, end_date=None):
        return sum(t["valore"] for t in self.get_transactions_by_client(client_name, start_date, end_date))